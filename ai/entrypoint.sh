#!/bin/sh

uvicorn src.ai_api:app --host 0.0.0.0 --port 5000 &

while true
do
  sleep 86400
  echo "[CRON] $(date): Günlük AI blog başlığı işleniyor..."
  python ai/scripts/dispatch_one_job.py
done