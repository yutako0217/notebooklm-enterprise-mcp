from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

def batch_delete_notebooks(notebook_ids: list[str]) -> dict:
    """
    Deletes one or more notebooks in a batch.

    Args:
        notebook_ids: A list of notebook IDs to delete.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    # Construct the full resource names for the API call.
    names = [
        f"projects/{project_number}/locations/{location}/notebooks/{notebook_id}"
        for notebook_id in notebook_ids
    ]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks:batchDelete"
    
    api_request_body = {
        "names": names
    }

    return make_api_request("POST", endpoint, payload=api_request_body)
