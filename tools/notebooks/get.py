from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

def get_notebook(notebook_id: str) -> dict:
    """
    Retrieves a specific notebook by its ID.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks/{notebook_id}"

    return make_api_request("GET", endpoint)
