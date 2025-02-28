#!/bin/bash

set -ex

black main.py src tests
ruff check --fix main.py src tests
mypy --strict main.py src tests