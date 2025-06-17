"""
utils.py
---------
Утилиты и вспомогательные функции для краулера.
"""


from urllib.parse import urlparse, urljoin
import re

def is_valid_url(url: str, allowed_domain: str) -> bool:
    """
    Проверяет, что URL валиден, использует http/https и принадлежит allowed_domain.

    :param url: Проверяемый URL
    :param allowed_domain: Домен, разрешённый для обхода
    :return: True если URL валиден и принадлежит allowed_domain, иначе False
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if parsed.netloc != allowed_domain:
            return False
        # Дополнительная проверка на валидность домена (простейшая)
        if not re.match(r"^[a-zA-Z0-9.-]+$", parsed.netloc):
            return False
        return True
    except Exception:
        return False

def normalize_url(base_url: str, link: str) -> str:
    """
    Приводит ссылку к абсолютному URL относительно base_url.

    :param base_url: Базовый URL страницы, где нашли ссылку
    :param link: Ссылка, найденная на странице (может быть относительной)
    :return: Абсолютный URL
    """
    return urljoin(base_url, link)

def safe_put(queue, item, timeout=1):
    """
    Безопасно кладет элемент в очередь с таймаутом.
    Возвращает True, если успешно, False если очередь полна.

    :param queue: multiprocessing.Queue или подобная
    :param item: элемент для добавления
    :param timeout: время ожидания
    """
    try:
        queue.put(item, timeout=timeout)
        return True
    except Exception:
        return False

def safe_get(queue, timeout=1):
    """
    Безопасно получает элемент из очереди с таймаутом.
    Возвращает элемент, либо None если очередь пуста.

    :param queue: multiprocessing.Queue или подобная
    :param timeout: время ожидания
    """
    try:
        return queue.get(timeout=timeout)
    except Exception:
        return None

