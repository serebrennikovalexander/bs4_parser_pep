import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_DOC_URL
from exceptions import ParserFindListWithTagException
from outputs import control_output
from utils import check_response, find_tag, get_response


def whats_new(session):

    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    check_response(response, whats_new_url)
    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        "li",
        attrs={"class": "toctree-l1"}
    )
    results = [("Ссылка на статью", "Заголовок", "Редактор, автор")]

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, "a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            # Если страница не загрузится, программа перейдёт
            # к следующей ссылке.
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    check_response(response, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, features="lxml")
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
        else:
            raise ParserFindListWithTagException(
                "Список с нужными тегами не найден"
            )
    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is None:
            version = a_tag.text
            status = ""
        else:
            version = text_match.group("version")
            status = text_match.group("status")
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    check_response(response, downloads_url)
    soup = BeautifulSoup(response.text, features="lxml")
    table_tag = find_tag(soup, "table", attrs={"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag,
        "a",
        attrs={"href": re.compile(r".+pdf-a4\.zip$")}
    )
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, "wb") as file:
        file.write(response.content)

    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    response = get_response(session, PEP_DOC_URL)
    check_response(response, PEP_DOC_URL)
    soup = BeautifulSoup(response.text, features="lxml")
    main_section = find_tag(soup, "section", attrs={"id": "numerical-index"})
    main_table = find_tag(
        main_section,
        "table",
        attrs={"class": "pep-zero-table docutils align-default"},
    )
    main_table_body = find_tag(main_table, "tbody")
    list_of_pep = main_table_body.find_all(
        "tr", attrs={"class": ["row-even", "row-odd"]}
    )

    all_pep_numbers = 0
    number_of_pep = {}
    logging_info = []

    for pep in tqdm(list_of_pep):
        all_pep_numbers += 1

        # Поиск статуса на странице PEP.
        link_a_tag = pep.find("a")
        href = link_a_tag["href"]
        version_link = urljoin(PEP_DOC_URL, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        dl_tag = find_tag(
            soup,
            "dl",
            attrs={"class": "rfc2822 field-list simple"}
        )
        dt_tags = dl_tag.find_all("dt")
        for tag in dt_tags:
            if tag.text == "Status:":
                previous_tag = tag
                break
        status_tag = previous_tag.find_next_sibling("dd")
        status_on_page = status_tag.string

        # Поиск статуса PEP в общем списке.
        first_column_tag = find_tag(pep, "abbr")
        preview_status = first_column_tag.text[1:]

        # Сравнение статуса на странице PEP со статусом в общем списке.
        try:
            expected_status = EXPECTED_STATUS[preview_status]
        except KeyError:
            logging_info.append(
                f"Статуса {preview_status} нет среди ключей словаря"
            )
            continue

        if status_on_page not in expected_status:
            logging_info.extend(
                [
                    f"Несовпадающие статусы: {version_link}",
                    f"Статус в карточке: {status_on_page}",
                    f"Ожидаемые статусы: {EXPECTED_STATUS[preview_status]}",
                ]
            )
            status_on_page = EXPECTED_STATUS[preview_status][0]

        # Подсчёт количества документов с каждым статусом.
        number_of_pep[status_on_page] = (number_of_pep.get(status_on_page, 0)
                                         + 1)

    for log in logging_info:
        logging.info(log)

    # Создание таблицы с результатами.
    results = [("Статус", "Количество")]
    results.extend(number_of_pep.items())

    results.append(("Total", all_pep_numbers))

    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")
    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)

    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
