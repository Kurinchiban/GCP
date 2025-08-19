from google.cloud import pubsub_v1
import os

# Set the SA key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/kurinchiban/Desktop/GCP/pubsub/sa_key.json"

project_id = "661664371282"
subscription_id = "demo-topic-sub" 

# Create subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()  # acknowledge the message so it’s not re-delivered

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

# Keep the main thread alive so subscriber keeps running
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
