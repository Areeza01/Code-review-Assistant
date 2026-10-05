import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

blob_service = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

CONTAINER_NAME = "code-files"

def upload_to_blob(file_path, file_name):

    container_client = blob_service.get_container_client(
        CONTAINER_NAME
    )

    with open(file_path, "rb") as data:

        container_client.upload_blob(
            name=file_name,
            data=data,
            overwrite=True
        )

    return True
