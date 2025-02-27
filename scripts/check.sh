#!/bin/bash

set -ex
echo

black main.py src tests
echo

ruff check --fix main.py src tests
echo

mypy --strict main.py src tests
echo
