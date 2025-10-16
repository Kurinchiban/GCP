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
        project="stoked-brand-474706-u8",
        region="us-central1",
        temp_location="gs://pubsub-dataflow-project-10/dataflow/user_event/temp",
        staging_location="gs://pubsub-dataflow-project-10/dataflow/user_event/staging",
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
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription="projects/stoked-brand-474706-u8/subscriptions/user-event-topic-sub")
            | "Parse JSON" >> beam.ParDo(ParseMessage())
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table="user_event_pubsub_dataflow_dataset.user_event",
                schema=table_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

if __name__ == "__main__":
    run()
        
