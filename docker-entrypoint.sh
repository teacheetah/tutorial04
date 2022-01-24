#!/bin/bash
set -eo pipefail
shopt -s nullglob

export PATH=${PATH}:/teacheetah
export PYTHONPATH=${PYTHONPATH}:/teacheetah

cd /teacheetah

cd apps && alembic upgrade head && cd ../

# TODO: comment this line for production deployment
exec gunicorn --bind 0.0.0.0:8000 main:init_app --reload --worker-class aiohttp.GunicornWebWorker --access-logfile '-'

# TODO: use the below command for produciton
# exec gunicorn --bind 0.0.0.0:8000 main:init_app --worker-class aiohttp.GunicornWebWorker --access-logfile '-'
