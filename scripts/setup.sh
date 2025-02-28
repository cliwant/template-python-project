#!/bin/bash

set -ex

virtualenv venv --python=python3.13
source venv/bin/activate

pip install --upgrade pip black ruff mypy pylint pytest pre-commit 'watchdog[watchmedo]'
pip install --requirement requirements.txt

pre-commit install