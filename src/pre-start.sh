#!/bin/bash

# Получение абсолютного пути к каталогу скрипта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Переход в корневой каталог проекта
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Путь до директории с проектом
PROJECT_DIR="$PROJECT_ROOT/src"

# Путь до файла settings
SETTINGS_FILE="$PROJECT_DIR/settings.py"

# Экспорт PYTHONPATH
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Запуск скрипта base_data.py и передача пути к settings в качестве аргумента
python3 "$PROJECT_DIR/scripts/base_data.py" "--settings-file=$SETTINGS_FILE"