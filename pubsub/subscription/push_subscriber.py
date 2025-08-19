from fastapi import FastAPI, Request
import base64
import json

app = FastAPI()

@app.post("/push-handler")
async def receive_pubsub_message(request: Request):
    envelope = await request.json()
    print(f"Raw message from Pub/Sub: {envelope}")

    if not envelope or "message" not in envelope:
        return {"status": "Bad Request"}

    pubsub_message = envelope["message"]

    # Decode message data
    data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
    print(f"Decoded message: {data}")

    # If attributes are included
    attributes = pubsub_message.get("attributes", {})
    print(f"Attributes: {attributes}")

    # Always return 200 OK to acknowledge delivery
    return {"status": "ok"}


# Steps

# uvicorn push_subscriber:app --host 0.0.0.0 --port 8080
# ngrok http 8080
# https://aa720dd6b43e.ngrok-free.app/
# https://aa720dd6b43e.ngrok-free.app/push-handler