#!/usr/bin/env bash

set -e

cd "${0%/*}/.."

echo "running isort checks..."
isort . --check --settings-path ./pyproject.toml

exit $?
