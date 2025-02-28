#!/bin/bash

set -ex

# 실행 환경 인자 받아서 환경변수로 설정
export PROFILE="$1"

watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./scripts/check.sh && python main.py" \
    --drop \
    .