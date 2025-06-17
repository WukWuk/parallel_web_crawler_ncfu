import threading
from queue import Queue, Empty
from crawler.worker import crawl_page


class CrawlerController:
    def __init__(self, start_url: str, num_workers: int, max_depth: int, max_pages: int, stop_flag=None):
        self.start_url = start_url
        self.num_workers = num_workers
        self.max_depth = max_depth
        self.max_pages = max_pages

        self.task_queue = Queue()
        self.visited = set()
        self.lock = threading.Lock()
        self.stats = {}  # worker_id -> count of pages visited
        self.stop_flag = stop_flag  # callable, чтобы проверить, остановлен ли процесс

    def worker_func(self, worker_id: int):
        visited_count = 0
        while True:
            if self.stop_flag and self.stop_flag():
                break
            try:
                url, depth = self.task_queue.get(timeout=1)
            except Empty:
                break

            with self.lock:
                if url in self.visited:
                    self.task_queue.task_done()
                    continue
                self.visited.add(url)

            crawl_result = crawl_page(url, depth)
            visited_count += 1

            if depth < self.max_depth:
                for link in crawl_result:
                    with self.lock:
                        if len(self.visited) >= self.max_pages:
                            break
                        if link not in self.visited:
                            self.task_queue.put((link, depth + 1))

            self.task_queue.task_done()

            with self.lock:
                if len(self.visited) >= self.max_pages:
                    break

        with self.lock:
            self.stats[worker_id] = visited_count

    def start(self):
        self.task_queue.put((self.start_url, 0))
        threads = []

        for worker_id in range(self.num_workers):
            t = threading.Thread(target=self.worker_func, args=(worker_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
