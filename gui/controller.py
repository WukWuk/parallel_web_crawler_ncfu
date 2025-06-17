# gui/controller.py

from PyQt5.QtWidgets import QMessageBox

class CrawlController:
    def __init__(self, parent_window):
        self.parent = parent_window

    def start_crawling(self, url, workers, depth):
        # Здесь пока просто выводим параметры — потом добавим запуск краулера
        print(f"Starting crawl:\nURL: {url}\nWorkers: {workers}\nDepth: {depth}")

        QMessageBox.information(self.parent, "Started", f"Crawling started for:\n{url}\nWorkers: {workers}, Depth: {depth}")
