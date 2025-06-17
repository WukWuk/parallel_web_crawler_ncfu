"""
config.py
----------
Настройки и параметры для параллельного веб-краулера.
Можно расширять для чтения из файла или командной строки.
"""


import multiprocessing

# Стартовая страница для краулинга
START_URL = "https://en.wikipedia.org/wiki/Web_crawler"

# Максимальная глубина обхода ссылок (чтобы не уходить слишком далеко)
MAX_DEPTH = 2

# Максимальное количество параллельных процессов (воркеров)
MAX_PROCESSES = max(2, multiprocessing.cpu_count() - 1)  # по умолчанию — число ядер минус один

# Таймаут ожидания HTTP-запроса (в секундах)
HTTP_TIMEOUT = 5

# Максимальное количество страниц для обхода (ограничение)
MAX_PAGES = 100

# Логирование: уровни DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# User-Agent для HTTP-запросов (иногда сайты блокируют без него)
USER_AGENT = "ParallelCrawlerBot/1.0 (+https://github.com/yourusername/parallel_web_crawler)"

# Заголовки для HTTP-запросов
HEADERS = {
    "User-Agent": USER_AGENT,
}

# Максимальная длина очереди задач (чтобы не захламлять память)
TASK_QUEUE_MAXSIZE = 1000

# Проверять ссылки только с этим доменом
def get_allowed_domain():
    from urllib.parse import urlparse
    return urlparse(START_URL).netloc

ALLOWED_DOMAIN = get_allowed_domain()

