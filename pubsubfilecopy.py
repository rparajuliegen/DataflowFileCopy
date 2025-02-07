import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.cloud import storage
import json

class CopyFile(beam.DoFn):
    def __init__(self, target_bucket):
        self.target_bucket = target_bucket
        self.storage_client = None

    def process(self, message):
        from google.cloud import storage
        try:
            
            if self.storage_client is None:  # Check if it's already initialized
                self.storage_client = storage.Client()
            # Decode the Pub/Sub message (it's a JSON string)
            message_dict = json.loads(message.decode('utf-8'))

            # Extract bucket and file path from the message
            source_bucket_name = message_dict['bucket']
            source_file_path = message_dict['name'] # Path within the source bucket

            print(f"Copying gs://{source_bucket_name}/{source_file_path} to gs://{self.target_bucket}")

            source_bucket = self.storage_client.bucket(source_bucket_name)
            source_blob = source_bucket.blob(source_file_path)

            target_bucket_obj = self.storage_client.bucket(self.target_bucket)

            # Keep the same file path in the target bucket
            target_file_path = source_file_path  
            target_blob = target_bucket_obj.blob(target_file_path)

            # Copy the file
            ##source_blob.copy_to(target_blob, if_generation_match=0) copy_to fails, switcehd to download as string

            blob_data = source_blob.download_as_string()  
            print("SRC data is : ",blob_data)
            target_blob.upload_from_string(blob_data)

            yield f"Copied gs://{source_bucket_name}/{source_file_path} to gs://{self.target_bucket}/{target_file_path}"

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing message: {message}. Error: {e}")
            # Handle error appropriately (dead-letter queue, etc.)
            raise 
        except Exception as e:
            print(f"Error copying file: {e}") # More general error message
            # Handle error appropriately (dead-letter queue, etc.)
            raise  


class PubSubToGCSOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--input_topic',
            type=str,
            help='Pub/Sub topic to read from.'
        )
        parser.add_value_provider_argument(
            '--target_bucket',
            type=str,
            help='GCS bucket to copy files to (e.g., targetbucket123).'
        )


def run(argv=None):
    pipeline_options = PipelineOptions(argv)
    pipeline_options.view_as(StandardOptions).streaming = True  # Important for Pub/Sub

    options = pipeline_options.view_as(PubSubToGCSOptions)
    target_bucket = options.target_bucket.get()
    input_topic = options.input_topic.get()  # Get the input topic string value

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(topic=input_topic).with_output_types(bytes) # Use the retrieved value
            | 'CopyFile' >> beam.ParDo(CopyFile(target_bucket)) # Use the retrieved value
            | 'Log' >> beam.Map(print)
        )

if __name__ == '__main__':
    run()