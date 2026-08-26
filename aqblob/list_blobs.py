from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
import logging

logger = logging.getLogger(__name__)


def list_blobs(
    az_storage_connection_string: str,
    az_storage_container_name: str,
    prefix: str,
) -> list[str]:
    """
    List blobs in an Azure Blob Storage container with a given prefix.

    Args:
        az_storage_connection_string (str): Azure Storage connection string.
        az_storage_container_name (str): Name of the Azure Storage container.
        prefix (str): Prefix to filter blobs.

    Returns:
        list[str]: List of blob names matching the prefix.
    """
    try:
        with BlobServiceClient.from_connection_string(
            az_storage_connection_string,
        ) as blob_service_client:
            container_client = blob_service_client.get_container_client(
                az_storage_container_name
            )
            blob_list = container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blob_list]

    except (AzureError, OSError) as e:
        logger.error(
            "Failed to list blobs with prefix %s in container %s: %s",
            prefix,
            az_storage_container_name,
            e,
        )
        raise
