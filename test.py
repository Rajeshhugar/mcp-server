


#### ----------------------------------

from fastmcp import FastMCP
import random
import json


mcp = FastMCP("Simple Calculator Server")

@mcp.tool
def add(a:int, b:int) -> int:
    """Add two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The sum of the two numbers.
    """
    return a + b


@mcp.tool
def random_number(min:int=1, max:int=100) -> int:
    """Generate a random number between min and max.
    
    Args:
        min (int): The minimum value.
        max (int): The maximum value.
    
    Returns:
        int: A random number between min and max.
    """
    return random.randint(min, max)



@mcp.resource("info://server")
def server_info() -> str:
    """Get information about the server."""

    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A simple calculator server.",
        "tools": list(mcp.tools.keys()),
        "authors": ["Rajesh Hugar"],
    }
    return json.dumps(info, indent=2)



if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)