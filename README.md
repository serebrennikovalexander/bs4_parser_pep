# Парсер документации Python
### Описание
Парсер помогает собирать различную информацию с официально страницы языка Python.
У парсера есть 4 режима работы:
1) Собирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей.
2) Собирать информацию о статусах версий Python.
3) Скачивать архив с актуальной документацией.
4) Посчитать количество PEP в каждом статусе и общее количество PEP.
### Технологии
Python 3.10
Beautiful Soup 4.9.3
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:serebrennikovalexander/bs4_parser_pep.git
```

```
cd bs4_parser
```

Cоздать и активировать виртуальное окружение:

```
python3.10 -m venv venv
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip3 install -r requirements.txt
```

Перейти в папку src:

```
cd bs4_parser
```

Запустить проект:
Режим 1
```
python3 main whats-new
```
Режим 2
```
python3 main latest-versions
```
Режим 3
```
python3 main download
```
Режим 4
```
python3 main pep
```
Ещё есть опциональные аргументы:
-h, --help - Вызов справки
-c, --clear-cache - Очистка кеша
-o {pretty,file}, --output {pretty,file} - Дополнительные способы вывода данных.
pretty - вывод таблицы в терминале
file - сохранение в csv-файл в папку resulta
Пример использования допольнительных аргументоа
```
python3 main pep --output file
```
### Автор
Александр Серебренников
