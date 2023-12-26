"""Utils for the Google Cloud Secret Manager."""


from google.cloud import secretmanager

from .gcp import PROJECT_ID, get_credentials


def get_client() -> secretmanager.SecretManagerServiceClient:
    """Get a client for the Google Cloud Secret Manager."""
    return secretmanager.SecretManagerServiceClient(credentials=get_credentials())


def encrypt_secret(
    client: secretmanager.SecretManagerServiceClient, secret_id: str, secret_value: str
) -> None:
    """Encrypt a secret string and store it in the Secret Manager.

    Creates a new secret version for the given secret ID.
    If the secret does not exist, it is created.

    Args:
        client: The Secret Manager client.
        secret_id: The ID of the secret to encrypt.
        secret_value: The secret string to encrypt.
    """
    client = get_client()

    try:
        client.get_secret(request={"name": client.secret_path(PROJECT_ID, secret_id)})

    except Exception as e:
        if "404 Secret" in str(e):
            client.create_secret(
                request={
                    "parent": f"projects/{PROJECT_ID}",
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
        else:
            raise e

    client.add_secret_version(
        request={
            "parent": f"projects/{PROJECT_ID}/secrets/{secret_id}",
            "payload": {"data": secret_value.encode("UTF-8")},
        }
    )


def decrypt_secret(
    client: secretmanager.SecretManagerServiceClient, secret_id: str
) -> str:
    """Decrypt a secret string from the Secret Manager.

    Args:
        client: The Secret Manager client.
        secret_id: The ID of the secret to decrypt.

    Returns:
        The decrypted secret string.
    """
    client = get_client()
    name = client.secret_version_path(PROJECT_ID, secret_id, "latest")
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
