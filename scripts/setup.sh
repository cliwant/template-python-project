#!/bin/bash

set -ex

virtualenv venv --python=python3.13
source venv/bin/activate

pip install --upgrade pip black ruff mypy pylint pytest 'watchdog[watchmedo]'
pip install --requirement requirements.txt