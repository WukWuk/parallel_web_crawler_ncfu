"""
parser.py
----------
Парсинг HTML страниц и извлечение ссылок.
"""

from bs4 import BeautifulSoup
from crawler.utils import normalize_url, is_valid_url
from crawler.config import ALLOWED_DOMAIN

def extract_links(html_content: str, base_url: str) -> set:
    """
    Извлекает уникальные валидные ссылки из HTML контента.

    :param html_content: HTML страницы в виде строки
    :param base_url: URL страницы, относительно которого нормализуем ссылки
    :return: Множество уникальных абсолютных ссылок, удовлетворяющих условиям
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = set()

    for a_tag in soup.find_all('a', href=True):
        raw_link = a_tag['href']
        absolute_link = normalize_url(base_url, raw_link)

        if is_valid_url(absolute_link, ALLOWED_DOMAIN):
            links.add(absolute_link)

    return links
