#!/usr/bin/env bash
set -e
source /usr/bin/datayes-init

while read line
do
    echo ${line}
    export ${line}
done < /tmp/consul.env

echo "finish export envs , update"

cd  ${DATA_PROD_HOME}/data_prd_mineiwang

python  ./recall_salesfilter.py

