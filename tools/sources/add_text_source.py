from services.gcp import get_gcp_settings
# Note: We need to import from the notebooks common module as it contains the generic request handler.
from tools.notebooks.notebooklm_client import make_api_request

def add_text_source_to_notebook(notebook_id: str, source_name: str, content: str) -> None:
    """
    Adds a new text-based data source to a notebook.

    Args:
        notebook_id: The ID of the notebook to add the source to.
        source_name: A display name for the new source.
        content: The raw text content of the source.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks/{notebook_id}/sources:batchCreate"
    
    api_request_body = {
        "userContents": [
            {
                "textContent": {
                    "sourceName": source_name,
                    "content": content
                }
            }
        ]
    }

    make_api_request("POST", endpoint, payload=api_request_body)
