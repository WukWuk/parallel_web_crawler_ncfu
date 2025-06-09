"""
visualizer.py
--------------
Простой консольный прогресс-бар для краулера.
"""


import sys

def print_progress(current: int, total: int, bar_length: int = 40):
    """
    Выводит прогресс в консоль в виде прогресс-бара.

    :param current: текущий прогресс (например, количество посещённых страниц)
    :param total: общее количество (например, лимит страниц)
    :param bar_length: длина прогресс-бара в символах
    """
    if total == 0:
        percent = 0
    else:
        percent = current / total

    filled_length = int(bar_length * percent)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rПрогресс: |{bar}| {current}/{total} страниц')
    sys.stdout.flush()

    if current >= total:
        print()  # Перевод строки при завершении
