#!/usr/bin/env bash

BASE=~/src/github/DCGM
source $BASE/venv3.8/bin/activate
(
cd ..
export PYTHONPATH=$PWD/pero-ocr:$PWD/pero_ocr_web
)
export TF_CUDNN_USE_AUTOTUNE=0

LOG_DATE=$(date '+%Y%m%d%H%M%S')
while true
do
    python3 -u $BASE/pero-ocr-api/processing_client/run_client.py -c $BASE/pero-ocr-api/processing_client/config-example.ini --time-limit 0.3 --exit-on-done 2>&1 | tee -a api.$LOG_DATE.txt
    sleep 2
    python -u run_clients.py --time-limit 0.02 2>&1 | tee -a log.$LOG_DATE.txt
    sleep 2
done

