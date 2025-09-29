from google.cloud import secretmanager
import json

def get_gcp_secret(secret_id: str, project_id: str, version: str = "latest") -> dict:
    """
    Fetch a secret from GCP Secret Manager and return it as a dictionary.

    Args:
        secret_id (str): The name of the secret in Secret Manager.
        project_id (str): Your GCP project ID.
        version (str): Secret version, default is "latest".

    Returns:
        dict: The secret key-value pairs.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    
    response = client.access_secret_version(name=secret_name)
    secret_string = response.payload.data.decode("UTF-8")
    
    return json.loads(secret_string)


# Example usage
if __name__ == "__main__":
    project_id = "elt-pipeline-465809"
    secret_id = "etl-pipeline-template"

    secrets = get_gcp_secret(secret_id, project_id)
    print(secrets)

    # Access individual keys
    ENV = secrets["ENV"]
    DB_HOST = secrets["DB_HOST"]
    DB_USER = secrets["DB_USER"]
    DB_PASS = secrets["DB_PASS"]
    DB_NAME = secrets["DB_NAME"]

    print(f"ENV={ENV}, DB_HOST={DB_HOST}, DB_USER={DB_USER}")
