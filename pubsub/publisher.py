from google.cloud import pubsub_v1
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/kurinchiban/Desktop/GCP/pubsub/sa_key.json"

project_id = "661664371282"
topic_id = "demo-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = {"user": "Kurinji", "action": "practice PubSub"}
future = publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
print(f"Published message ID: {future.result()}")   