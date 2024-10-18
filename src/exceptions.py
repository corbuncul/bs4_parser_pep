"""Модуль исключений парсера."""


class ParsingError(Exception):
    """Вызывается при сбое парсинга."""


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class NothingToParseError(Exception):
    """Вызывается при отсутствии необходимой информации."""
