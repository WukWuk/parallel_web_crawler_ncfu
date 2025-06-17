from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QTextEdit,
    QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from gui.crawler_worker_thread import CrawlerWorkerThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Без стандартного заголовка
        self.setFixedSize(600, 450)
        self.worker_thread = None
        self.mouse_drag_pos = None  # Для перетаскивания окна

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Черный кастомный заголовок ---
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #0d0d0d;")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)

        title_label = QLabel("Parallel Web Crawler")
        title_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e57373;
                border: none;
                font-size: 16pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff1744;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        title_bar.setLayout(title_layout)
        main_layout.addWidget(title_bar)
        # -----------------------------------

        # Ввод ссылки
        url_layout = QHBoxLayout()
        url_label = QLabel("Start URL:")
        url_label.setStyleSheet("color: white; font-weight: bold;")
        self.url_input = QLineEdit()
        self.url_input.setText("")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # Кол-во воркеров
        workers_layout = QHBoxLayout()
        workers_label = QLabel("Number of Workers:")
        workers_label.setStyleSheet("color: white; font-weight: bold;")
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 20)
        self.workers_spin.setValue(4)
        workers_layout.addWidget(workers_label)
        workers_layout.addWidget(self.workers_spin)
        main_layout.addLayout(workers_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        main_layout.addLayout(buttons_layout)

        # Прогрессбар
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Логи и статистика
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)

        # Связываем сигналы
        self.start_button.clicked.connect(self.start_crawling)
        self.stop_button.clicked.connect(self.stop_crawling)

        # Стили для текста в основном окне (чтобы был белый на темном фоне)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QSpinBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #2962ff;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
            }
            QProgressBar {
                background-color: #1e1e1e;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2962ff;
                border-radius: 5px;
            }
        """)

    # Реализация перетаскивания окна по клику на заголовок (и по всему окну, как в твоём примере)
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.mouse_drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mouse_drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    # Остальной функционал без изменений
    def start_crawling(self):
        start_url = self.url_input.text()
        num_workers = self.workers_spin.value()

        if not start_url.startswith("http"):
            self.log_output.append("Error: URL must start with http or https")
            return

        self.log_output.clear()
        self.log_output.append(f"Starting crawl from: {start_url} with {num_workers} workers")

        self.worker_thread = CrawlerWorkerThread(start_url, num_workers)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished_with_stats.connect(self.on_crawling_finished)
        self.worker_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_crawling(self):
        if self.worker_thread:
            self.worker_thread.stop()
            self.log_output.append("Stopping crawling...")
            self.stop_button.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.log_output.append(f"Progress: {value}%")

    def on_crawling_finished(self, stats):
        self.log_output.append("Crawling finished!")
        total_pages = sum(stats.values())
        self.log_output.append(f"Total pages crawled: {total_pages}")
        for worker_id, count in stats.items():
            self.log_output.append(f"Worker {worker_id}: {count} pages")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(100)
