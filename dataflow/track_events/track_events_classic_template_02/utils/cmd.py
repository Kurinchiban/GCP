# export GOOGLE_APPLICATION_CREDENTIALS="/home/kurinchiban/Desktop/GCP/dataflow/sa_key.json"

# python3 pubsub_to_bq.py \
#   --runner DataflowRunner \
#   --project stoked-brand-474706-u8 \
#   --region us-central1 \
#   --staging_location gs://pubsub-dataflow-project-10/dataflow/classic_template/user_event/staging \
#   --temp_location gs://pubsub-dataflow-project-10/dataflow/classic_template/user_event/temp \
#   --template_location gs://pubsub-dataflow-project-10/dataflow/classic_template/templates/user_event_template \
#   --input_subscription projects/stoked-brand-474706-u8/subscriptions/user-event-topic-sub \
#   --output_table stoked-brand-474706-u8:analytics.user_event


# python3 pubsub_to_bq.py \
#   --runner DataflowRunner \
#   --project stoked-brand-474706-u8 \
#   --staging_location gs://pubsub-dataflow-project-10/dataflow/classic_template/user_event/staging \
#   --template_location gs://pubsub-dataflow-project-10/dataflow/classic_template/templates/user_event_template \
#   --region us-central1 


# gcloud dataflow jobs run user-event-job-1 \
#   --gcs-location gs://pubsub-dataflow-project-10/dataflow/classic_template/templates/user_event_template \
#   --region us-central1 \
#   --parameters input_subscription=projects/stoked-brand-474706-u8/subscriptions/user-event-topic-sub,\
# output_table=stoked-brand-474706-u8:user_event_pubsub_dataflow_dataset.user_event