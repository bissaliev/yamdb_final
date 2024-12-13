"""
Скрипт для автоматической установки пакета django-debug-toolbar
и установки всех необходимых настроек
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = "api_yamdb"
DEBUG_TOOLBAR = "django-debug-toolbar"
REQUIREMENT_FILE = "requirements.txt"


def read_file(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def write_in_file(file_path: str, data):
    with open(file_path, "w", encoding="utf-8") as writer:
        writer.writelines(data)


def is_installed_debug_toolbar(file_path: str):
    lines = read_file(file_path)
    return any(DEBUG_TOOLBAR in line for line in lines)


def uninstall_debug_toolbar():
    os.system(f"pip uninstall {DEBUG_TOOLBAR}")
    os.system(f"pip freeze > {REQUIREMENT_FILE}")


def install_toolbar():
    os.system(f"pip install {DEBUG_TOOLBAR}")
    os.system(f"pip freeze > {REQUIREMENT_FILE}")


def add_debug_toolbar_in_settings(file):
    lines = read_file(file)
    update_lines = []
    for line in lines:
        update_lines.append(line)
        if "INSTALLED_APPS" in line:
            update_lines.append('    "debug_toolbar",\n')
        csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware"
        if csrf_middleware in line:
            update_lines.append(
                '    "debug_toolbar.middleware.DebugToolbarMiddleware",\n'
            )
    if not any("INTERNAL_IPS" in line for line in update_lines):
        update_lines.append('\nINTERNAL_IPS = ["127.0.0.1"]\n')
    write_in_file(file, update_lines)


def add_debug_toolbar_to_urlconf(file):
    update = (
        "\nif settings.DEBUG:\n"
        "    import debug_toolbar\n"
        "    urlpatterns += "
        '(path("__debug__/", include(debug_toolbar.urls)),)\n'
    )
    lines = read_file(file)
    is_settings = False
    is_debug = False
    for line in lines:
        if "from django.conf import settings" in line:
            is_settings = True
        if "__debug__/" in line:
            is_debug = True
    if not is_settings:
        lines = ["from django.conf import settings\n"] + lines
    if not is_debug:
        lines += update
    write_in_file(file, update)


if __name__ == "__main__":
    settings_file = os.path.join(
        BASE_DIR, PROJECT_NAME, PROJECT_NAME, "settings.py"
    )
    urls_file = os.path.join(BASE_DIR, PROJECT_NAME, PROJECT_NAME, "urls.py")
    requirements_file = os.path.join(BASE_DIR, "requirements.txt")
    if not is_installed_debug_toolbar(requirements_file):
        install_toolbar()
        print("Приложение установлено успешно.")
        add_debug_toolbar_in_settings(settings_file)
        print("Настройки записаны в файл settings.py.")
        add_debug_toolbar_to_urlconf(urls_file)
        print("Настройки записаны в файл urls.py.")
    else:
        print("Приложение уже установлено.")
