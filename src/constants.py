"""Костанты парсера."""

from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
"""Базовая страница с документацией Python для парсера."""

PEP_DOC_URL = 'https://peps.python.org/'
"""Страница с документацией PEP."""

BASE_DIR = Path(__file__).parent
"""Рабочая директория."""

DOWNLOAD_DIR = BASE_DIR / 'downloads'
"""Директория для скачивания."""

RESULTS_DIR = BASE_DIR / 'results'
"""Директория с результатами парсинга."""

LOG_DIR = BASE_DIR / 'logs'
"""Директория с логами."""

LOG_FILE = LOG_DIR / 'parser.log'
"""Файл для логов."""

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
"""Формат вывода в логи."""

DT_FORMAT = '%d.%m.%Y %H:%M:%S'
"""Формат даты/времени для логов"""

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
"""Формат даты/времени для файлов CSV."""

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
"""Статусы документов PEP."""

PRETTY = 'pretty'
"""Режим для вывода в таблицу на консоль."""

FILE = 'file'
"""Режим для вывода в файл."""

DEFAULT = ''
"""Режим по умолчанию. Простой вывод на консоль."""

CHOICES = (PRETTY, FILE)
"""Выбор из режимов."""
