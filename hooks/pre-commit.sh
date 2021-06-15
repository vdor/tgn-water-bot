#!/usr/bin/env bash

echo "Running pre-commit hook..."
source ./venv/bin/activate

./hooks/run-black-check.sh
if [ $? -ne 0 ]; then
    echo "Black checker reported errors, commit aborted. Execute 'black .' for autoformatting"
    exit 1
fi

./hooks/run-isort-check.sh
if [ $? -ne 0 ]; then
    echo "isort checker reported errors, commit aborted. Execute 'isort .' to fix imports"
    exit 1
fi

./hooks/run-mypy-check.sh
if [ $? -ne 0 ]; then
    echo "Mypy checker reported errors, commit aborted."
    exit 1
fi
