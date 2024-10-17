"""Парсинг информации о версиях Python и PEP."""

import logging
import re
from urllib.parse import urljoin

from requests import RequestException
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import EXPECTED_STATUS, MAIN_DOC_URL, PEP_DOC_URL, DOWNLOAD_DIR
from exceptions import GetResponseError, NothingToParseError
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    """Парсинг обновлений."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    error_msg = ''

    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        try:
            soup = get_soup(session, version_link)
        except (RequestException, GetResponseError) as error:
            error_msg += f'{error}\n'
            continue
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    if error_msg != '':
        logging.error(error_msg, exc_info=True)
    return results


def latest_versions(session):
    """Парсинг последних версий."""
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise NothingToParseError('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]

    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    """Скачивание документации."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOAD_DIR / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info('Архив был загружен и сохранён: %s', archive_path)


def pep(session):
    """Парсинг иформации о статусах PEP."""
    soup = get_soup(session, PEP_DOC_URL)
    index_by_category = find_tag(soup, 'section', {'id': 'index-by-category'})
    tbody_tags = index_by_category.find_all('tbody')
    tbody_tags_list = [tbody_tag.find_all('tr') for tbody_tag in tbody_tags]
    rows_tag = []
    for item in tbody_tags_list:
        rows_tag.extend(item)
    total = 0
    results = [('Статус', 'Количество')]
    statuses = {
        'Active': 0,
        'Accepted': 0,
        'Deferred': 0,
        'Final': 0,
        'Provisional': 0,
        'Rejected': 0,
        'Superseded': 0,
        'Withdrawn': 0,
        'Draft': 0,
    }
    info_msg = ''
    error_msg = ''
    for row in tqdm(rows_tag):
        abbr_tag = find_tag(row, 'abbr')
        status_in_table = abbr_tag.text[1:]
        a_tag = find_tag(row, 'a')
        pep_url = urljoin(PEP_DOC_URL, a_tag['href'])
        try:
            soup = get_soup(session, pep_url)
        except (RequestException, GetResponseError) as error:
            error_msg += f'{error}\n'
            continue
        dl_tag = find_tag(soup, 'dl', {'class': 'rfc2822'})
        dt_all = dl_tag.find_all('dt')
        status = ''
        for dt_tag in dt_all:
            if 'Status' in dt_tag.text:
                status = dt_tag.find_next_sibling('dd').text
                break
        if status not in EXPECTED_STATUS[status_in_table]:
            info_msg += (
                f'Несовпадающие статусы: {pep_url} '
                f'Статус в карточке: {status} '
                f'Ожидаемые статусы: {EXPECTED_STATUS[status_in_table]}'
            )
        statuses[status] = statuses.get(status, 0) + 1
        total += 1
    if error_msg != '':
        logging.error(error_msg, exc_info=True)
    if info_msg != '':
        logging.info(info_msg)
    results += statuses.items()
    results += [('Total', total)]
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Запуск функций в зависимости от аргументов."""
    try:
        configure_logging()
        logging.info('Парсер запущен!')

        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info('Аргументы командной строки: %s', args)

        session = requests_cache.CachedSession()

        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error('Произошла ошибка: %s', error)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
