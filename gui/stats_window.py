from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget


class StatisticsWindow(QWidget):
    def __init__(self, stats: dict):
        super().__init__()
        self.setWindowTitle("Crawl Statistics")
        self.setFixedSize(300, 400)
        self.init_ui(stats)

    def init_ui(self, stats: dict):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Pages visited by each worker:"))

        stats_list = QListWidget()
        for worker_id, count in stats.items():
            stats_list.addItem(f"Worker {worker_id}: {count} pages")

        layout.addWidget(stats_list)
        self.setLayout(layout)
