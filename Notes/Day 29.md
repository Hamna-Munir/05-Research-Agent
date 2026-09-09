# Day 29 — AI Agent Fundamentals

**Objective:** Understand what an AI agent actually is, and how it's different from a normal LLM application.

---

## 📖 Theory

### LLM vs AI Agent

Every project so far (Weeks 1–4) has been an **LLM application**: user sends input, the model processes it, a response comes back — one direct step. An **AI agent** is different: it's given a **goal**, and it decides for itself what steps to take to achieve that goal — which might include calling tools, gathering information, or taking several steps before producing a final answer.

The key shift: in an LLM application, the developer controls the logic path. In an agent, the *model itself* decides the path, based on the situation.

### Agent architecture

An agent typically consists of: a goal (what it's trying to accomplish), access to tools (functions it can call), a reasoning loop (deciding what to do next), and a way to track its own progress (agent state).

### The agent loop

```
Goal
 ↓
Think / Decide
 ↓
Action
 ↓
Tool
 ↓
Observation
 ↓
Decide Again
 ↓
Final Answer
```

This loop can repeat multiple times — the agent isn't limited to one tool call. It thinks, acts, observes the result, and decides whether it needs to act again or if it has enough to answer.

### Tools

A tool is a function the agent can choose to call — a calculator, a search function, a database query, anything with defined inputs and outputs. The agent doesn't need to know *how* the tool works internally, only *what* it does and *when* it's useful.

### Observations and Actions

- **Action** — the agent's decision to do something (e.g., "call the calculator tool with these numbers").
- **Observation** — the result that comes back from that action, which the agent then uses to decide its next step.

### Agent state

Agent state is what the agent currently knows and has done so far in the loop — previous actions, observations, and progress toward the goal. Without tracking state, the agent would have no memory of what it already tried.

### Autonomous vs deterministic workflows

A **deterministic workflow** follows the exact same steps every time, regardless of input (e.g., a fixed if/else chain). An **autonomous** agent's steps vary based on the specific situation — the same agent might use zero tools for a simple question and three tools for a complex one, because it decided that dynamically rather than following a fixed script.

---

## 🎥 Best Resource

One high-quality introductory video on "AI Agents + Agentic AI + Tool Calling" — avoid watching multiple videos and losing time on repeated introductory content.

## 📚 Reading

Read the introductory function/tool calling section of your LLM provider's official documentation (e.g., OpenAI or Groq's function calling guide).

---

## 💻 Coding Exercise

Simulate a simple agent decision process:

```
User: What is 25 × 35?

Agent:
→ Identify calculation task
→ Select calculator tool
→ Call calculator
→ Receive result
→ Return answer
```

---

## 🛠 Mini Project — Calculator Agent

Build an agent with 4 tools:

```python
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Cannot divide by zero"
```

The LLM should decide which tool to call based on the user's question, rather than the code parsing the math itself.

---

## 🧠 Quiz

1. What's the core difference between an LLM application and an AI agent?
2. What is a tool, in the context of agents?
3. Describe the agent loop in your own words.
4. Why does an agent need tools instead of just answering from its own knowledge?
5. What's the difference between an action and an observation?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus Challenge

Add a `calculate_percentage()` tool and confirm the agent correctly picks it over the other four when asked a percentage-based question.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| LLM tries to do the calculation itself instead of calling the tool | Tool descriptions aren't clear/specific enough for the model to recognize when to use them | Write clear, specific tool descriptions stating exactly what each tool does |
| Incorrect tool schema | Tool definition doesn't match what the LLM API expects (missing required fields) | Follow the exact schema format required by your provider's function-calling API |
| Tool arguments mismatch | The model calls the tool with different argument names/types than the function expects | Keep function signatures and tool schema argument names identical |
| Tool errors not handled | Dividing by zero, missing arguments, etc. crash the whole agent loop | Wrap tool execution in error handling and return a message the LLM can work with, not a crash |

---

## ✅ Checklist

- [ ] Agent concept understood
- [ ] Agent loop understood
- [ ] Tool calling understood
- [ ] Calculator tools built (add, subtract, multiply, divide)
- [ ] LLM connected to tools
- [ ] Multiple test cases run
- [ ] Git commit made

---

## 📂 GitHub Push

```bash
git add .
git commit -m "feat: build calculator agent with tool calling"
git push
```

Repository: `05-Research-Agent/`

---

## 📝 Journal

*Write about: What makes an AI system an agent?*

---

## ⭐ Daily Skill Learned

AI Agent Fundamentals + Tool Calling
