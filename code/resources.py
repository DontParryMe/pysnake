import os
import sys

import os
import sys


def resource_path(relative_path):
    """ Возвращает правильный путь для доступа к ресурсам,
    который работает как для разработки, так и для однофайлового исполняемого файла. """
    # Если скрипт запущен PyInstaller'ом
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Если скрипт запущен напрямую
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Дополнительный шаг: подняться на уровень вверх, чтобы путь был относительно корня проекта
        base_path = os.path.dirname(base_path)

    return os.path.join(base_path, relative_path)
