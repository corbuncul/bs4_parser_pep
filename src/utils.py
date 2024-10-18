"""Модуль вспомогательных инструментов парсера."""

import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParsingError, ParserFindTagException


def get_response(session, url, encoding='urf-8'):
    """Получение ответа от сервера с обработкой ошибок."""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as e:
        error_msg = f'Возникла ошибка при загрузке страницы {url}.'
        raise ParsingError(error_msg) from e


def find_tag(soup, tag, attrs=None):
    """Поиск тегов с обработкой ошибок."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url, features='lxml'):
    response = get_response(session, url)
    return BeautifulSoup(response.text, features=features)
