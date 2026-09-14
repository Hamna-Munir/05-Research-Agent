"""
tools.py
Day 29 -> calculator tools (add, subtract, multiply, divide, percentage)
Day 30 -> utility tools (get_current_date, calculate, word_count) + schemas
Day 31 -> search tool (DuckDuckGo, no API key needed)

Every tool is wrapped in error handling so a bad argument or a failed
search never crashes the whole agent loop — it returns an error string
the LLM can work with instead.
"""

from datetime import date
from duckduckgo_search import DDGS


# ---------------------------------------------------------------------------
# Day 29 — Calculator tools
# ---------------------------------------------------------------------------

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float):
    if b == 0:
        return "Error: cannot divide by zero."
    return a / b


def calculate_percentage(part: float, whole: float):
    if whole == 0:
        return "Error: whole cannot be zero."
    return (part / whole) * 100


# ---------------------------------------------------------------------------
# Day 30 — Utility tools
# ---------------------------------------------------------------------------

def get_current_date() -> str:
    return str(date.today())


def word_count(text: str):
    if not text or not text.strip():
        return "Error: no text provided."
    return len(text.split())


# ---------------------------------------------------------------------------
# Day 31 — Search tool
# ---------------------------------------------------------------------------

def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the web and returns a list of results, each with a title,
    snippet, and URL — preserving sources rather than discarding them.

    Args:
        query: the search query.
        max_results: how many results to return.

    Returns:
        A list of dicts with 'title', 'snippet', 'url', or an error dict
        if the search itself fails.
    """
    if not query or not query.strip():
        return [{"error": "Empty search query."}]

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", ""),
            }
            for r in results
        ]
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


# ---------------------------------------------------------------------------
# Tool registry + schemas (used by agent.py for tool calling)
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "calculate_percentage": calculate_percentage,
    "get_current_date": get_current_date,
    "word_count": word_count,
    "web_search": web_search,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Adds two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtracts the second number from the first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiplies two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divides the first number by the second.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_percentage",
            "description": "Calculates what percentage 'part' is of 'whole'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "part": {"type": "number"},
                    "whole": {"type": "number"},
                },
                "required": ["part", "whole"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Returns today's date.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "word_count",
            "description": "Counts the number of words in a piece of text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Searches the web for current or specific information not "
                "already known. Returns a list of results with titles, "
                "snippets, and source URLs."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                    "max_results": {"type": "integer", "description": "Number of results to return."},
                },
                "required": ["query"],
            },
        },
    },
]


def execute_tool(tool_name: str, arguments: dict):
    """
    Safely executes a tool by name with the given arguments.
    Never raises — always returns a result or an error string, so a
    single bad tool call can't crash the agent loop.
    """
    if tool_name not in TOOL_FUNCTIONS:
        return f"Error: unknown tool '{tool_name}'."

    try:
        return TOOL_FUNCTIONS[tool_name](**arguments)
    except Exception as e:
        return f"Error executing '{tool_name}': {str(e)}"
