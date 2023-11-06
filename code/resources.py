import os
import sys


def resource_path(relative_path):
    """ Возвращает правильный путь для доступа к ресурсам,
    который работает как для разработки, так и для однофайлового исполняемого файла. """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)
