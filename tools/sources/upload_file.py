from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request_with_file_upload


def upload_file(notebook_id: str, file_path: str, display_name: str) -> dict:
    """
    Uploads a file to a notebook in NotebookLM Enterprise.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks/{notebook_id}/sources:uploadFile"

    return make_api_request_with_file_upload(endpoint, file_path, display_name)
