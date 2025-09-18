import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions

class ParseMessage(beam.DoFn):
    def process(self, element):
        import json
        record = json.loads(element.decode("utf-8"))
        # Must return a dict matching BigQuery schema
        yield {
            "name": record.get("name"),
            "event_type": record.get("event_type"),
            "event_timestamp": record.get("event_timestamp"),
        }

def run():
    # Configure pipeline options
    options = PipelineOptions(
        runner="DataflowRunner",
        project="pratice-gcp-service",
        region="us-central1",
        temp_location="gs://gcp-practice-012/Dataflow/user_event/temp",
        staging_location="gs://gcp-practice-012/Dataflow/user_event/staging",
        streaming=True, 
    )
    options.view_as(StandardOptions).streaming = True

    # Define BigQuery table schema
    table_schema = {
        "fields": [
            {"name": "name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "event_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "event_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ]
    }

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription="projects/pratice-gcp-service/subscriptions/user_event-sub")
            | "Parse JSON" >> beam.ParDo(ParseMessage())
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table="analytics.user_event",
                schema=table_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

if __name__ == "__main__":
    run()
        
# export GOOGLE_APPLICATION_CREDENTIALS="/home/kurinchiban/Desktop/GCP/dataflow/sa_key.json"

# python3 pubsub_to_bq.py \
#   --runner=DataflowRunner \
#   --project=pratice-gcp-service \
#   --region=us-central1 \
#   --temp_location=gs://gcp-practice-012/Dataflow/user_event/temp \
#   --staging_location=gs://gcp-practice-012/Dataflow/user_event/staging \
#   --job_name=pubsub-to-bq-job-$(date +%Y%m%d-%H%M%S) 

# gcloud pubsub topics publish user_event \
#   --project=pratice-gcp-service \
#   --message '{"name":"Alice","event_type":"login","event_timestamp":"2025-09-17T09:15:00Z"}'

# gcloud dataflow jobs cancel 2025-09-17_04_02_44-7670517525870377359 \
#   --project=pratice-gcp-service \
#   --region=us-central1