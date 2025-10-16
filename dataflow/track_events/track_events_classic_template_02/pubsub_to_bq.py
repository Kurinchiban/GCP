import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import SetupOptions, StandardOptions, PipelineOptions


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

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_subscription',
        help='Pub/Sub subscription to read from'
    )
    parser.add_argument(
        '--output_table',
        help='BigQuery table to write to <project>:<dataset>.<table>'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    options = PipelineOptions(pipeline_args)
    options.view_as(StandardOptions).streaming = True
    options.view_as(SetupOptions).save_main_session = True

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
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(
                subscription=known_args.input_subscription
            )
            | "Parse JSON" >> beam.ParDo(ParseMessage())
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table=known_args.output_table,
                schema=table_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )