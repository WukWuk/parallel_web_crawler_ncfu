"""
run_crawler.py
---------------
Скрипт для запуска параллельного веб-краулера.
"""

from crawler.manager import manager
from crawler.logger import log

def main():
    log.info("Старт параллельного веб-краулера.")
    manager()
    log.info("Краулер завершил работу.")

if __name__ == "__main__":
    main()
