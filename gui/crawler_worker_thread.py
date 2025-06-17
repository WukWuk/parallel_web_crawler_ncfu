from PyQt5.QtCore import QThread, pyqtSignal
from crawler.crawler_controller import CrawlerController


class CrawlerWorkerThread(QThread):
    progress_updated = pyqtSignal(int)  # прогресс в процентах
    finished_with_stats = pyqtSignal(dict)

    def __init__(self, start_url, num_workers, max_depth=2, max_pages=100):
        super().__init__()
        self.start_url = start_url
        self.num_workers = num_workers
        self.max_depth = max_depth
        self.max_pages = max_pages

        self._should_stop = False

    def run(self):
        def stop_flag():
            return self._should_stop

        controller = CrawlerController(
            start_url=self.start_url,
            num_workers=self.num_workers,
            max_depth=self.max_depth,
            max_pages=self.max_pages,
            stop_flag=stop_flag
        )

        # Запускаем краулер в отдельном потоке
        # Чтобы отправлять прогресс — запустим контроллер в своём потоке,
        # но контроллер запускает потоки на Python threading.
        # Мы просто периодически эмитим прогресс из here:
        import time
        import threading

        thread = threading.Thread(target=controller.start)
        thread.start()

        while thread.is_alive():
            visited_count = len(controller.visited)
            progress_percent = int(visited_count / self.max_pages * 100)
            if progress_percent > 100:
                progress_percent = 100
            self.progress_updated.emit(progress_percent)
            if self._should_stop:
                break
            time.sleep(0.3)

        thread.join()
        self.finished_with_stats.emit(controller.stats)

    def stop(self):
        self._should_stop = True
