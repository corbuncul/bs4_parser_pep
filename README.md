# Проект парсинга pep
Проект позволяет получить информацию с сайтов https://docs.python.org/3/ и https://peps.python.org/
## Возможности
### Whats new
Позволяет получить ссылки на новости и обновления, названия статей, авторов и редакторов статей.
### Latest versions
Позволяет получить сведения о последних версиях Python
### Download
Позволяет скачать документацию по Python последней версии
### PEP
Позволяет получить инвормацию о статусах документов PEP
## Для запуска проекта необходимо:
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:corbuncul/bs4_parser_pep.git
cd bs4_parser_pep
```
- Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
- Перейти в директорию src:
```
cd src/
```
- Запустить проект в одном из режимов, например:
```
python3 main.py whats-new -o pretty
```
## Аргументы командной строки:
- режим работы:
1. whats-new
2. latest-versions
3. download
4. pep
- опциональные аргументы:
1. -h - вывод справки по аргументам командной строки
2. -c - запуска парсера с очисткой кеша
3. -o - Дополнительные способы вывода (pretty - в виде таблицы в консоль, file - в виде файла CSV)
