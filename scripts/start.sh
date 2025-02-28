#!/bin/bash

set -ex

watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./scripts/check.sh && python main.py" \
    --drop \
    .