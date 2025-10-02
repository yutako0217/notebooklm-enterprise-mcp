from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import all the tool functions
from tools.notebooks.create import create_notebook
from tools.notebooks.get import get_notebook
from tools.notebooks.list_recently_viewed import list_recently_viewed_notebooks
from tools.notebooks.batch_delete import batch_delete_notebooks
from tools.notebooks.share import share_notebook
from tools.sources.add_text_source import add_text_source_to_notebook
from tools.sources.batch_delete import batch_delete_sources_from_notebook

# Load environment variables from .env file
load_dotenv()

# Create an MCP server instance
mcp = FastMCP(
    name="Python MCP Application for NotebookLM",
)

# Register all the tool functions with the MCP server
mcp.add_tool(create_notebook)
mcp.add_tool(get_notebook)
mcp.add_tool(list_recently_viewed_notebooks)
mcp.add_tool(batch_delete_notebooks)
mcp.add_tool(share_notebook)
mcp.add_tool(add_text_source_to_notebook)
mcp.add_tool(batch_delete_sources_from_notebook)


if __name__ == "__main__":
    print("Starting MCP server for NotebookLM Tools...")
    print("To interact with the server, use the MCP CLI or a compatible client.")
    mcp.run()