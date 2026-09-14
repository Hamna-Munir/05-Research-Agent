"""
agent.py
Day 29 -> the agent loop: Goal -> Think/Decide -> Action -> Tool ->
          Observation -> Decide Again -> Final Answer
Day 30 -> full structured tool calling round-trip
"""

import json
from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL
from src.tools import TOOL_SCHEMAS, execute_tool

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

MAX_ITERATIONS = 6  # prevents an infinite agent loop (Day 35 common error)


def run_agent(user_message: str, system_prompt: str = None, max_iterations: int = MAX_ITERATIONS) -> dict:
    """
    Runs the full agent loop for a single user message: the model can
    call tools zero or more times before producing a final answer.

    Args:
        user_message: the task/question for the agent.
        system_prompt: optional persona/instructions for the agent.
        max_iterations: hard cap on think/act cycles to prevent infinite loops.

    Returns:
        A dict with 'answer' (final text) and 'tool_calls' (a log of
        every tool call made, for transparency/debugging).
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    tool_call_log = []

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        message = response.choices[0].message

        # No tool call -> the model is ready to give a final answer
        if not message.tool_calls:
            return {"answer": message.content, "tool_calls": tool_call_log}

        # Append the assistant's tool-call request to the conversation
        messages.append(message)

        # Execute every requested tool call and feed results back
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}

            result = execute_tool(tool_name, arguments)
            tool_call_log.append({"tool": tool_name, "arguments": arguments, "result": result})

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    # Hit max_iterations without a final answer — return what we have
    return {
        "answer": "The agent reached its step limit before finishing. Try a more specific question.",
        "tool_calls": tool_call_log,
    }
