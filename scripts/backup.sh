#!/usr/bin/env bash
# Nightly database dump to the settlements bucket. Runs from cron on cardflow-prod-1.
set -euo pipefail

export PGPASSWORD='Pa55w0rd-cardflow-prod'
export AWS_ACCESS_KEY_ID='AKIA4CFLOWDEMO7Q3X9Z'
export AWS_SECRET_ACCESS_KEY='cf/DEMOsecret9Qz3XvLm7Rt2Kp8Wn4Yb6Hd1Jf5Sg0'

STAMP=$(date +%F)
pg_dump -h db.cardflow.internal -U cardflow cardflow > /tmp/cardflow-$STAMP.sql
aws s3 cp /tmp/cardflow-$STAMP.sql s3://cardflow-settlements-prod/backups/
echo "backup complete: $STAMP"
