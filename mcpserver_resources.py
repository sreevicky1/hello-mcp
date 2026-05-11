import json
from fastmcp import FastMCP

mcp = FastMCP(name="data-server")

# Resource returning content from Indian culture file
@mcp.resource("resource://indian_culture")
def get_indian_culture() -> str:
    """Provides information about Indian culture from knowledge base."""
    with open("C:/Users/Lucifer/python_workspace/coding_ninja/module3_agents/session8_mcp/indian_culture.json", "r") as f:
        culture_data = json.load(f)
    
    return json.dumps(culture_data, indent=2)

# Resource returning JSON data (dict is auto-serialized)
@mcp.resource("data://config")
def get_myconfig() -> dict:
    """Provides application configuration as JSON."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="stdio")