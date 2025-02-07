#!/bin/bash
### This script createa an empty file with file name of current timestamp; 
### The file is then copied over to the GCS bucket
### File creation/copy happens randomly anywhere between 1 to 10 seconds to introduce some variability to pubsub.
### Script runs until explicity killed.
while true; do 
    sleep_time=$((RANDOM % 10 + 1))
    sleep $sleep_time
    timestamp=$(date +%Y%m%d_%H%M%S)
    touch "$timestamp.txt"
    echo "File '$timestamp.txt' created after sleeping for $sleep_time seconds."
    gcloud storage cp ./"$timestamp.txt" gs://egen_demo_bucket1/staging/"$timestamp.txt"
done
