from services.gcp import get_gcp_settings
from tools.notebooks.notebooklm_client import make_api_request

# Define the valid roles for sharing.
VALID_ROLES = ["OWNER", "WRITER", "READER", "NOT_SHARED"]

def share_notebook(notebook_id: str, email: str, role: str) -> dict:
    """
    Shares a notebook with a user, assigning them a specific role.

    Args:
        notebook_id: The ID of the notebook to share.
        email: The email address of the user to share with.
        role: The role to assign. Must be one of: OWNER, WRITER, READER, NOT_SHARED.
    """
    if role.upper() not in VALID_ROLES:
        raise ValueError(f"Invalid role '{role}'. Must be one of {VALID_ROLES}")

    gcp_settings = get_gcp_settings()
    project_number = gcp_settings["project_number"]
    location = gcp_settings["location"]

    endpoint = f"/projects/{project_number}/locations/{location}/notebooks/{notebook_id}:share"
    
    api_request_body = {
        "accountAndRoles": [
            {
                "email": email,
                "role": f"PROJECT_ROLE_{role.upper()}"
            }
        ]
    }

    return make_api_request("POST", endpoint, payload=api_request_body)
