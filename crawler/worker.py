"""
worker.py
----------
Воркеры — скачивают страницы, парсят и возвращают найденные ссылки.
"""

import requests
from crawler.parser import extract_links
from crawler.config import HTTP_TIMEOUT, HEADERS, MAX_PAGES
from crawler.logger import log

def crawl_page(url: str, depth: int):
    """
    Скачивает страницу и парсит ссылки.

    :param url: URL страницы для краулинга
    :param depth: текущая глубина обхода
    :return: множество ссылок или пустое множество при ошибке
    """
    try:
        log.debug(f"Запрос страницы: {url}")
        response = requests.get(url, timeout=HTTP_TIMEOUT, headers=HEADERS)
        if response.status_code != 200:
            log.warning(f"Неудачный статус {response.status_code} для {url}")
            return set()

        links = extract_links(response.text, url)
        log.info(f"Обработана страница {url} (найдено ссылок: {len(links)})")
        return links

    except requests.RequestException as e:
        log.error(f"Ошибка запроса {url}: {e}")
        return set()
    except Exception as e:
        log.error(f"Ошибка обработки {url}: {e}")
        return set()

def worker(task_queue, result_queue, visited, max_pages):
    """
    Основной воркер: берёт URL из task_queue, обрабатывает, кладёт результат в result_queue.

    :param task_queue: очередь задач (URL + глубина)
    :param result_queue: очередь результатов (URL + найденные ссылки + глубина)
    :param visited: общий словарь посещённых URL (shared dict)
    :param max_pages: максимальное количество страниц для обхода
    """
    while True:
        if len(visited) >= max_pages:
            log.info("Достигнут лимит по количеству страниц, завершаем воркер.")
            break

        try:
            url, depth = task_queue.get(timeout=3)
        except Exception:
            # Очередь пуста — выходим
            log.debug("Очередь задач пуста, воркер завершает работу.")
            break

        if url in visited:
            log.debug(f"Уже посещено: {url}")
            continue

        visited[url] = True

        links = crawl_page(url, depth)
        result_queue.put((url, links, depth))

