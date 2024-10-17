"""Костанты парсера."""
from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
"""Базовая страница с документацией Python для парсера."""

PEP_DOC_URL = 'https://peps.python.org/'
"""Страница с документацией PEP."""

BASE_DIR = Path(__file__).parent
"""Рабочая директория."""

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
"""Формат даты/времени для логов."""

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
