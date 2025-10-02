from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

def batch_delete_sources_from_notebook(notebook_id: str, source_ids: list[str]) -> dict:
    """
    Deletes one or more data sources from a notebook in a batch.

    Args:
        notebook_id: The ID of the notebook to delete sources from.
        source_ids: A list of source IDs to delete.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    # Construct the full resource names for the API call.
    names = [
        f"projects/{project_number}/locations/{location}/notebooks/{notebook_id}/sources/{source_id}"
        for source_id in source_ids
    ]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks/{notebook_id}/sources:batchDelete"
    
    api_request_body = {
        "names": names
    }

    return make_api_request("POST", endpoint, payload=api_request_body)
