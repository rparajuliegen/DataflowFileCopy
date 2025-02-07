#!/bin/bash

while true; do 
    sleep_time=$((RANDOM % 10 + 1))
    sleep $sleep_time
    timestamp=$(date +%Y%m%d_%H%M%S)
    touch "$timestamp.txt"
    echo "File '$timestamp.txt' created after sleeping for $sleep_time seconds."
    gcloud storage cp ./"$timestamp.txt" gs://egen_demo_bucket1/staging/"$timestamp.txt"
done