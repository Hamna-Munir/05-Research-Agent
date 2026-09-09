# Day 30 — Tool Calling

**Objective:** Learn to let the LLM use external functions/tools properly — going beyond a single calculator to a general tool-calling pattern.

---

## 📖 Theory

### Function calling

Function calling (also called tool calling) is a feature most modern LLM APIs support: instead of only returning text, the model can return a structured request to call a specific function with specific arguments. The application code then actually runs that function and sends the result back to the model, which uses it to form a final response.

### Tool schema

A tool schema is a structured description of a function that's given to the LLM — its name, what it does, and what parameters it accepts (with types). This is how the model knows the tool exists and when it might be useful, without ever seeing the function's actual code.

```python
{
    "name": "get_current_date",
    "description": "Returns today's date.",
    "parameters": {"type": "object", "properties": {}}
}
```

### Tool arguments

When the model decides to call a tool, it returns the arguments it wants to pass — as structured data (usually JSON), not free text. The application code parses these arguments and calls the real Python function with them.

### Tool execution

Tool execution is the actual running of the Python function, using the arguments the model provided. This happens in your code, not inside the LLM — the model only *decides* to call a tool; it never runs it directly.

### Tool response

After executing the tool, the result is sent back to the LLM as part of the conversation (typically as a special "tool" role message). The model then uses this result to generate its final, human-readable response.

### Structured tool calls

The full round-trip:

```
User
 ↓
LLM
 ↓
Tool Decision
 ↓
Function
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response
```

### Multiple tools

An LLM can be given several tools at once and will pick whichever one (or none) fits the user's request. This requires each tool to have a clear, distinct description — overlapping or vague descriptions make it harder for the model to choose correctly.

---

## 🎥 Best Resource

Search: "LLM Function Calling / Tool Calling Tutorial" — one focused video or the official docs' function-calling guide.

---

## 💻 Coding Exercise

Create 3 tools:

```python
def get_current_date():
    from datetime import date
    return str(date.today())

def calculate(expression: str):
    return eval(expression)  # simplified for learning; validate input in production

def word_count(text: str):
    return len(text.split())
```

Let the agent decide which tool fits the user's question — don't hardcode which tool gets called for which input.

---

## 🛠 Mini Project — Utility Agent

```
User:
How many words are in this paragraph?

Agent
↓
word_count()
↓
Result
↓
Answer
```

---

## 🧠 Quiz

1. What is a tool schema, and why does the LLM need one instead of just seeing the function code?
2. Does the LLM execute the function directly, or does something else happen?
3. Why is the tool's result sent back to the LLM instead of just showing it directly to the user?
4. How does an LLM manage choosing between multiple available tools?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus Challenge

Add proper error handling: if `calculate()` receives an invalid expression, or `word_count()` receives empty text, the tool should return a clear error message the LLM can relay to the user — not crash the whole agent.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Wrong parameter names | Tool schema's parameter names don't match the actual Python function's parameter names | Keep schema and function signatures identical |
| Invalid JSON arguments | The model's returned arguments aren't valid JSON (rare, but possible with some models) | Wrap argument parsing in a try/except and handle gracefully |
| Tool result not returned to the LLM | Tool executes successfully but the result is never sent back in the conversation | Confirm the tool result message is added to the conversation history before the next LLM call |
| Tool exception crashes the agent | An unhandled exception inside a tool function stops the whole process | Wrap every tool's execution in a try/except and return an error string instead of letting it crash |

---

## ✅ Checklist

- [ ] 3 tools built (get_current_date, calculate, word_count)
- [ ] Tool schemas written
- [ ] Tool execution implemented
- [ ] Error handling added
- [ ] Multiple tool tests run
- [ ] Git commit made

---

## 📂 GitHub Push

```bash
git add .
git commit -m "feat: implement reusable agent tools"
git push
```

---

## 📝 Journal

*Explain: What happens between an LLM deciding to use a tool and receiving the tool result?*

---

## ⭐ Daily Skill Learned

Function Calling + Tool Integration
