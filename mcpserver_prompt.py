from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent

# Create the MCP server
mcp = FastMCP(name="prompt-server")

# 1️⃣ Prompt: Ask for topic explanation
@mcp.prompt()
def explain_topic(topic: str) -> str:
    """Asks the model to explain a study topic"""
    return f"Explain the concept of '{topic}' in simple terms with a short example."

# 2️⃣ Prompt: Generate quiz questions
@mcp.prompt()
def generate_quiz(topic: str, difficulty: str = "easy") -> PromptMessage:
    """Asks the model to create a few quiz questions for a topic."""
    content = (
        f"Create 3 {difficulty}-level quiz questions about '{topic}'. "
        "Each question should have 4 options and specify the correct answer."
    )
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

# 3️⃣ Prompt: Summarize learning content
@mcp.prompt()
def summarize_notes(notes: str) -> PromptMessage:
    """Summarizes long notes into a short recap."""
    content = (
        f"Summarize the following notes into 3 bullet points for quick revision:\n\n{notes}"
    )
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

@mcp.tool()
def list_prompt_capabilities() -> str:
    return "Provides educational prompts like explain_topic, generate_quiz, summarize_notes."

if __name__ == "__main__":
    # Run the server in STDIO mode (works directly with Claude Desktop)
    mcp.run(transport="stdio")
