# Python MCP Application for NotebookLM

This is a Python application that provides tools compliant with the NotebookLM Enterprise API, using the Model Context Protocol (MCP).

## Setup

### 1. Prerequisites

- Python 3.9+
- Google Cloud SDK (`gcloud` command-line tool)

### 2. Google Cloud Authentication

Authenticate with Google Cloud to allow the application to make API calls on your behalf.

```bash
gcloud auth application-default login
```

### 3. Environment Variables

Create a `.env` file in the root of the project and add the necessary environment variables.

```env
# .env
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="your-gcp-location" # e.g., us-central1
```

Replace `"your-gcp-project-id"` with your actual Google Cloud Project ID. The application will automatically retrieve the corresponding Project Number.

### 4. Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
```

## Running the MCP Server

Once the setup is complete, you can run the MCP server from your terminal.

```bash
mcp run main.py
```

This command starts the server, making the defined tools available to compatible MCP clients.

## Connecting to an AI Assistant (e.g., Gemini CLI)

You can register this server as a tool provider for your AI assistant. The recommended way is to use the `gemini mcp add` command.

### Using the `gemini mcp add` Command

If you have the Gemini CLI installed, you can add this MCP server with a single command. Run the following from your project's root directory:

```bash
gemini mcp add notebooklm-tools mcp run main.py
```

- `notebooklm-tools`: This is the unique name we're giving our tool server.
- `mcp run main.py`: This is the command the Gemini CLI will use to start the server.

After running the command, you can verify the server was added by listing the configured MCP servers:

```bash
gemini mcp list
```

### Manual Configuration (using `mcp.json`)

Alternatively, for environments that support it (like VS Code with the Gemini extension), you can configure the tool server by creating a `mcp.json` file in your project's root directory.

1.  Create a file named `mcp.json`.

2.  Add the following content:

    ```json
    {
      "name": "NotebookLM Enterprise Tools",
      "description": "Tools for interacting with the NotebookLM Enterprise API.",
      "run": [
        "mcp",
        "run",
        "main.py"
      ]
    }
    ```

3.  Reload your AI assistant. It should now recognize the tools.

## Available Tools

This server provides the following tools to interact with the NotebookLM API.

### Notebook Management

- **`create_notebook(displayName: str)`**: Creates a new notebook.
- **`get_notebook(notebook_id: str)`**: Retrieves a specific notebook by its ID.
- **`list_recently_viewed_notebooks()`**: Lists recently viewed notebooks for the user.
- **`batch_delete_notebooks(notebook_ids: list[str])`**: Deletes one or more notebooks in a batch.
- **`share_notebook(notebook_id: str, email: str, role: str)`**: Shares a notebook with a user. Valid roles are `OWNER`, `WRITER`, `READER`, `NOT_SHARED`.

### Source Management

- **`add_text_source_to_notebook(notebook_id: str, source_name: str, content: str)`**: Adds a new text-based data source to a notebook.
- **`batch_delete_sources_from_notebook(notebook_id: str, source_ids: list[str])`**: Deletes one or more data sources from a notebook.
