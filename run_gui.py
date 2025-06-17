import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.crawler_worker_thread import CrawlerWorkerThread  # Мой поток
from PyQt5.QtGui import QFont

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
        }
        QLineEdit, QSpinBox {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333333;
            padding: 6px;
            border-radius: 6px;
        }
        QPushButton {
            background-color: #2962ff;
            color: white;
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0039cb;
        }
        QLabel {
            font-weight: bold;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: transparent;
        }
    """)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
