# DataflowFileCopy
POC to copy files from one bucket to another using DataFlow


## File List
### 1) filegeneration.sh
This is the script to create and copy the file to gcp source bucket.

### 2) requirements.txt
This requirement file is passed as parameter during job submission to handle any missing dependency in worker nodes.

### 3) pubsubfilecopy.py
This is the main file used to run the pipeline

## References
Use below command to submit the job. 

python3.11 pubsubfilecopy.py --input_topic=projects/level-strategy-450103-k6/topics/TOPIC_NAME output_path=gs://egen_demo_bucket1/pubsubtarget2/ --output_bucket=egen_demo_bucket1  --project=level-strategy-450103-k6 --temp_location=gs://egen_demo_bucket1/temp/  --staging_location=egen_demo_bucket1  --region=us-central1 --target_bucket=egen_demo_bucket_target --job_name=filecopyjob2 --runner=DataflowRunner --requirement_file ./requirements.txt --save_main_session
