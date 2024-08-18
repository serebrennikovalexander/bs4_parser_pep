# Парсер документации Python
### Описание
Парсер помогает собирать различную информацию с официально страницы языка Python.\
У парсера есть 4 режима работы:
1. Собирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей.
2. Собирать информацию о статусах версий Python.
3. Скачивать архив с актуальной документацией.
4. Посчитать количество PEP в каждом статусе и общее количество PEP.
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

Linux
```
python3 -m venv venv
source venv/bin/activate
```
Windows
```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

Linix
```
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```
Windows
```
python.exe -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Перейти в папку src:

```
cd src
```

Запустить проект:\
Режим 1\
Linux
```
python3 main.py whats-new
```
Windows
```
python main.py whats-new
```
Режим 2\
Linux
```
python3 main.py latest-versions
```
Windows
```
python main.py latest-versions
```
Режим 3\
Linux
```
python3 main.py download
```
Windows
```
python main.py download
```
Режим 4\
Linux
```
python3 main.py pep
```
Windows
```
python main.py pep
```
Ещё есть опциональные аргументы:\
```-h, --help``` - Вызов справки\
```-c, --clear-cache``` - Очистка кеша\
```-o {pretty,file}, --output {pretty,file}``` - Дополнительные способы вывода данных.\
```pretty``` - вывод таблицы в терминале (кроме режима 4)\
```file``` - сохранение в csv-файл в папку results\
Пример использования допольнительных аргументов:

Linux
```
python3 main.py pep --output file
```
Windows
```
python main.py pep --output file
```
### Автор
Александр Серебренников
