"""Модуль исключений парсера."""


class ParsingError(Exception):
    """Вызывается при сбое парсинга."""


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class GetResponseError(Exception):
    """Вызывается при ошибке получения ответа от сервера."""


class NothingToParseError(Exception):
    """Вызывается при отсутствии необходимой информации."""
