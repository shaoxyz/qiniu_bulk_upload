#!/usr/bin/env bash

python -m venv .

source bin/activate

pip install -r require.txt -i https://pypi.douban.com/simple

celery -B -A bulk_upload_service.celery_app worker -f tasks.log -D -l info

python bulk_upload_service/main.py