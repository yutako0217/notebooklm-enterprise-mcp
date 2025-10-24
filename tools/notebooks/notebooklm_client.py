import httpx
import google.auth
import google.auth.transport.requests
import mimetypes
from functools import lru_cache

from services.gcp import get_gcp_settings


@lru_cache(maxsize=2)
def get_base_api_url(upload: bool = False) -> str:
    """Constructs the base URL for the NotebookLM API using GCP settings.

    The URL is cached to avoid repeated calls to retrieve GCP settings.

    Returns:
        The base API URL as a string.
    """
    gcp_settings = get_gcp_settings()
    location = gcp_settings["location"]
    if upload:
        base_url = f"https://{location}-discoveryengine.googleapis.com/upload/v1alpha"
    else:
        base_url = f"https://{location}-discoveryengine.googleapis.com/v1alpha"
    print(f"Using base URL: {base_url}")
    return base_url


@lru_cache(maxsize=1)
def get_auth_token() -> str:
    """Obtains a Google Cloud authentication token.

    Caches the token to avoid repeated authentication calls.

    Returns:
        The authentication token as a string.

    Raises:
        Exception: If credentials are not valid or a token cannot be obtained.
    """
    credentials, _ = google.auth.default()
    # We need to manually refresh the credentials to get the access token.
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)

    if not credentials.valid or not credentials.token:
        raise Exception("Could not obtain valid credentials.")

    return credentials.token


def make_api_request(method: str, endpoint: str, payload: dict | None = None) -> dict:
    """Makes a request to the NotebookLM API.

    Args:
        method: The HTTP method (e.g., 'POST', 'GET', 'DELETE').
        endpoint: The API endpoint path (e.g., '/notebooks').
        payload: The JSON payload for the request body.

    Returns:
        The JSON response from the API as a dictionary.

    Raises:
        Exception: For API errors or unexpected issues.
    """
    try:
        token = get_auth_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        base_url = get_base_api_url(upload=False)
        url = f"{base_url}{endpoint}"

        with httpx.Client(timeout=30.0) as client:
            if payload:
                response = client.request(method, url, json=payload, headers=headers)
            else:
                response = client.request(method, url, headers=headers)
            print(response.status_code)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()

    except httpx.HTTPStatusError as e:
        # Forward the error response from the downstream API
        raise Exception(
            f"Error from NotebookLM API ({e.response.status_code}): {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def make_api_request_with_file_upload(
    endpoint: str, file_path: str, display_name: str
) -> dict:
    """Makes a file upload request to the NotebookLM API using raw upload.

    Args:
        endpoint: The API endpoint path.
        file_path: The path to the file to upload.
        display_name: The display name for the file.

    Returns:
        The JSON response from the API as a dictionary.

    Raises:
        Exception: For API errors or unexpected issues.
    """
    try:
        token = get_auth_token()
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Goog-Upload-File-Name": display_name,
            "X-Goog-Upload-Protocol": "raw",
            "Content-Type": content_type,
        }

        base_url = get_base_api_url(upload=True)
        url = f"{base_url}{endpoint}"

        with open(file_path, "rb") as f:
            file_content = f.read()
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, content=file_content, headers=headers)
                response.raise_for_status()
                return response.json()

    except httpx.HTTPStatusError as e:
        raise Exception(
            f"Error from NotebookLM API ({e.response.status_code}): {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
