#!/usr/bin/env bash

set -e

cd "${0%/*}/.."

echo "running pytest..."
pytest

exit $?
