from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

def create_notebook(title: str) -> dict:
    """
    Creates a new notebook in NotebookLM Enterprise.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks"
    
    # The request body sent to the NotebookLM API.
    api_request_body = {
        "notebook": {
            "title": title
        }
    }

    return make_api_request("POST", endpoint, payload=api_request_body)