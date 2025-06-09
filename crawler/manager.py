"""
manager.py
-----------
Менеджер краулера — координирует работу воркеров, управляет очередями и состоянием.
"""


import multiprocessing
import time
from crawler.config import START_URL, MAX_DEPTH, MAX_PAGES, MAX_PROCESSES, TASK_QUEUE_MAXSIZE
from crawler.worker import worker
from crawler.logger import log
from crawler.visualizer import print_progress  # <-- добавляем импорт

def manager():
    """
    Запускает краулер с многопроцессной архитектурой.
    """
    log.info("Запуск менеджера краулера...")

    # Очередь задач: элементы — (url, глубина)
    task_queue = multiprocessing.Queue(maxsize=TASK_QUEUE_MAXSIZE)

    # Очередь результатов: элементы — (url, найденные ссылки, глубина)
    result_queue = multiprocessing.Queue()

    # Общий словарь посещённых URL (shared между процессами)
    manager = multiprocessing.Manager()
    visited = manager.dict()

    # Добавляем стартовый URL с глубиной 0
    task_queue.put((START_URL, 0))

    # Запускаем воркеры
    processes = []
    for i in range(MAX_PROCESSES):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue, visited, MAX_PAGES), name=f"Worker-{i+1}")
        p.start()
        processes.append(p)
        log.info(f"Запущен {p.name}")

    try:
        while True:
            # Отрисовка прогресса:
            print_progress(len(visited), MAX_PAGES)

            # Завершаем, если достигли лимит по страницам
            if len(visited) >= MAX_PAGES:
                log.info("Достигнут лимит по количеству страниц, менеджер останавливает работу.")
                break

            try:
                url, links, depth = result_queue.get(timeout=5)
            except Exception:
                # Если воркеры закончили работу (очередь пуста)
                if all(not p.is_alive() for p in processes):
                    log.info("Все воркеры завершили работу, менеджер завершает цикл.")
                    break
                continue

            log.debug(f"Менеджер получил результат по {url} (глубина {depth}), добавляем ссылки...")

            if depth + 1 <= MAX_DEPTH:
                for link in links:
                    if link not in visited:
                        try:
                            task_queue.put_nowait((link, depth + 1))
                            log.debug(f"Добавлена задача: {link} (глубина {depth+1})")
                        except multiprocessing.queues.Full:
                            log.warning("Очередь задач переполнена, пропускаем некоторые ссылки.")
                            break

            time.sleep(0.01)  # Чтобы не гонять цикл слишком быстро

    except KeyboardInterrupt:
        log.info("Получен сигнал прерывания, останавливаем краулер...")

    finally:
        # Завершаем все процессы
        for p in processes:
            if p.is_alive():
                p.terminate()
                log.info(f"Завершён процесс {p.name}")

        print_progress(len(visited), MAX_PAGES)  # Финальный прогресс-бар
        log.info(f"Краулер завершил работу. Всего посещено страниц: {len(visited)}")

if __name__ == "__main__":
    manager()
