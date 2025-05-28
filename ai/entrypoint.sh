#!/bin/sh

# 1. FastAPI API başlatılır (arka planda)
uvicorn src.ai_api:app --host 0.0.0.0 --port 5000 &

# 2. Sonsuz döngü ile her gün bir blog başlığı işle
while true
do
  sleep 86400
  echo "[CRON] $(date): Günlük AI blog başlığı işleniyor..."
  python ai/scripts/dispatch_one_job.py
done