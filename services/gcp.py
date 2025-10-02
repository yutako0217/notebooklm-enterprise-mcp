import os
from functools import lru_cache

import google.auth
from googleapiclient import discovery
from googleapiclient.errors import HttpError

@lru_cache(maxsize=1)
def get_project_number(project_id: str) -> str | None:
    """Converts a GCP Project ID to a Project Number.

    Args:
        project_id: The GCP Project ID.

    Returns:
        The corresponding Project Number as a string, or None if an error occurs.
    """
    try:
        credentials, _ = google.auth.default()
        service = discovery.build(
            "cloudresourcemanager", "v1", credentials=credentials
        )
        request = service.projects().get(projectId=project_id)
        response = request.execute()
        return response.get("projectNumber")
    except HttpError as e:
        print(f"Error fetching project number for project ID '{project_id}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_gcp_settings():
    """Retrieves GCP settings from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id or project_id == "your-gcp-project-id":
        raise ValueError("GCP_PROJECT_ID environment variable is not set or is invalid.")
    if not location:
        raise ValueError("GCP_LOCATION environment variable is not set.")

    project_number = get_project_number(project_id)
    if not project_number:
        raise ValueError(f"Could not determine project number for project ID '{project_id}'.")

    return {
        "project_id": project_id,
        "project_number": project_number,
        "location": location,
    }
