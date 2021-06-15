#!/usr/bin/env bash

set -e

cd "${0%/*}/.."

echo "running mypy type checks..."
mypy . --ignore-missing-imports --exclude venv

exit $?
