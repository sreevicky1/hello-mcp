from fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("simple-math-server")

# Add a simple tool
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b * 2

@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of a and b
    """
    return a * b * 2

@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name.
    
    Args:
        name: The person's name
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to the MCP server."

# Add a resource
@mcp.resource("config://server")
def get_server_config():
    """Get server configuration information."""
    return {
        "name": "Simple Math Server",
        "version": "1.0.0",
        "description": "A simple MCP server for basic math operations"
    }

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="stdio")






