from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

def list_recently_viewed_notebooks() -> dict:
    """
    Lists recently viewed notebooks for the user.
    """
    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks:listRecentlyViewed"

    # The API supports a pageSize parameter, but we are omitting it for simplicity.
    return make_api_request("GET", endpoint)
