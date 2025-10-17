# export GOOGLE_APPLICATION_CREDENTIALS="/home/kurinchiban/Desktop/GCP/dataflow/sa_key.json"

# python3 pubsub_to_bq.py \
#   --runner=DataflowRunner \
#   --project=stoked-brand-474706-u8 \
#   --region=us-central1 \
#   --temp_location=gs://pubsub-dataflow-project-10/dataflow/user_event/temp \
#   --staging_location=gs://pubsub-dataflow-project-10/dataflow/user_event/staging \
#   --job_name=pubsub-to-bq-job-$(date +%Y%m%d-%H%M%S) 


# gcloud dataflow jobs cancel 2025-10-15_23_36_07-11898631943773723020 \
#   --project=stoked-brand-474706-u8 \
#   --region=us-central1

# Inject Data in PubSub

# gcloud pubsub topics publish user-event-topic \
#   --project=stoked-brand-474706-u8 \
#   --message '{"name":"Bob","event_type":"logout","event_timestamp":"2025-09-17T10:00:00Z"}'

# gcloud pubsub topics publish user-event-topic \
#   --project=stoked-brand-474706-u8 \
#   --message '{"name":"Charlie","event_type":"login","event_timestamp":"2025-09-17T10:30:00Z"}'

# gcloud pubsub topics publish user-event-topic \
#   --project=stoked-brand-474706-u8 \
#   --message '{"name":"Diana","event_type":"purchase","event_timestamp":"2025-09-17T11:00:00Z"}'

# gcloud pubsub topics publish user-event-topic \
#   --project=stoked-brand-474706-u8 \
#   --message '{"name":"Eve","event_type":"login","event_timestamp":"2025-09-17T11:15:00Z"}'

# gcloud pubsub topics publish user-event-topic \
#   --project=stoked-brand-474706-u8 \
#   --message '{"name":"Frank","event_type":"logout","event_timestamp":"2025-09-17T11:45:00Z"}'
