"""Модуль вывода результатов."""

import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    RESULTS_DIR,
    PRETTY,
    FILE,
    DEFAULT,
    CHOICES,
)


def default_output(*args):
    """Простой вывод результатов."""
    results = args[0]
    for row in results:
        print(*row)


def pretty_output(*args):
    """Вывод данных в консоль в виде таблицы."""
    results = args[0]
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(*args):
    """Вывод результатов в файл CSV."""
    results = args[0]
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = args[1].mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info('Файл с результатами был сохранён: %s', file_path)


OUTPUT_FUNCTIONS = {
    PRETTY: pretty_output,
    FILE: file_output,
    DEFAULT: default_output,
}


def control_output(results, cli_args):
    """Вывод данных в консоль или файл."""
    output = cli_args.output
    if output not in CHOICES:
        output = DEFAULT
    OUTPUT_FUNCTIONS[output](results, cli_args)
