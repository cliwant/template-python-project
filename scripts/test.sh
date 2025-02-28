#!/bin/bash

set -ex

pylint main.py src tests
pytest tests