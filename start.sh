#!/bin/bash
cd ../../../../../python-zulip-api
python3 ./tools/provision
. ./zulip-api-py3-venv/bin/activate

cd zulip_bots/zulip_bots/bots/exerciser_kg/
docker compose build && docker compose up -d
nohup python3 worker_exerciser_kg.py > zulip_worker.log 2>&1 &
nohup zulip-run-bot exerciser_kg --config-file zuliprc-exerciser-kg > zulip_bot.log 2>&1 &
