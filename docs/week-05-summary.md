# Week 05 Summary — AI Agents & Tool Calling

**Repository:** 05-Research-Agent
**Days covered:** Day 29 – Day 35

---

## 🎯 Goal Recap

Move beyond a direct LLM application (Weeks 1–4, where input goes in and a response comes straight back) to a real **AI agent** — a system that receives a goal, decides for itself which tools it needs, breaks a complex research question into smaller subtasks, gathers information, evaluates the reliability of what it finds, and produces a structured, evidence-based report.

---

## ✅ What Was Built

**AI Research Agent v1.0** — a full agentic research pipeline:

- A general-purpose **agent loop** (`agent.py`) implementing the Think → Act → Observe cycle, with a hard iteration cap to prevent infinite loops
- **8 tools** (`tools.py`): 5 calculator functions, `get_current_date`, `word_count`, and a web search tool (DuckDuckGo, no API key required) — every tool wrapped in error handling so a bad call never crashes the agent
- A **planner** (`planner.py`) that breaks a research question into 5-7 specific subtasks before any research begins
- A **researcher** (`researcher.py`) that executes each subtask via search, keeps source URLs attached to every finding, and synthesizes everything into a structured report (Executive Summary, Key Findings, Evidence, Sources, Limitations, Recommendation)
- An **evaluator** (`evaluator.py`) with automatic checks: does the report cite real sources, does it address the original question, does it follow the required structure
- A Streamlit UI (`app.py`) with a **Research Depth** control (Quick/Standard/Deep), trading off search thoroughness against speed
- Test coverage across tools, the agent loop, and the full research pipeline (25 tests total)

---

## 📖 What I Learned

- **An agent is defined by who controls the logic path.** In every previous week's project, the code decided what happened next. Here, the *model* decides — whether to call a tool, which one, and when it has enough information to stop. That's the real distinction between an LLM application and an agent, not just "it uses tools."
- **Tool schemas are a contract, not documentation.** The LLM never sees a tool's actual code — only its name, description, and parameter schema. A vague description directly causes wrong tool selection; this makes writing clear tool descriptions a real engineering task, not an afterthought.
- **The agent loop needs a stopping condition by design, not by luck.** Without a maximum iteration cap, there's nothing structurally preventing an agent from looping indefinitely if it keeps deciding "I need one more tool call." This has to be built in from the start, not patched in after something goes wrong.
- **Search results are raw material, not answers.** A search tool returns snippets and URLs — turning that into something useful requires summarizing, attaching sources, and (per Day 33) being honest when sources disagree instead of blending them into one falsely confident claim.
- **Planning before executing changes research quality.** Sending one vague question to a search tool produces vague results. Breaking it into 5-7 specific subtasks first — each independently searchable — produces far more usable, structured findings, mirroring how a human researcher would actually approach the same question.
- **Evaluating an agent is harder than evaluating a single prompt (Week 2) or a single retrieval call (Week 4).** An agent's output depends on a whole chain of decisions (which tools, how many searches, how it synthesized). A 15-question evaluation set spanning easy, complex, edge-case, and genuinely unanswerable questions is necessary to catch failures a handful of easy test questions would never reveal.

---

## 🐞 Design Challenges Worked Through

### 1. Preventing an unbounded agent loop
An agent that decides its own next step needs an explicit limit — otherwise a stuck reasoning pattern could call tools indefinitely. **Approach:** a hard `MAX_ITERATIONS` cap in `agent.py`, with a graceful fallback message if the limit is hit before a final answer is reached, rather than an unhandled infinite loop.

### 2. Keeping tool failures from crashing the whole agent
A single failed tool call (division by zero, an empty search query, a network error) shouldn't take down the entire research process. **Approach:** every tool function returns an error string on failure instead of raising an exception, and `execute_tool()` wraps execution in a try/except as a second layer of protection.

### 3. Preventing fabricated sources in the final report
Nothing stops a language model from generating a plausible-looking citation that was never actually retrieved. **Approach:** the synthesis prompt explicitly instructs the model to use only the provided findings and never invent sources, and `evaluator.py`'s `has_sources()` check cross-references the report against the actual URLs that were retrieved — a lightweight guard against fabricated citations making it into the final output undetected.

### 4. Respecting disagreement between sources instead of forcing a single answer
Real search results often don't agree with each other. The synthesis prompt (Day 33) explicitly instructs the model to present both views honestly when sources conflict, rather than averaging them into one falsely confident claim — this needed to be stated directly in the prompt, since the default behavior of most models is to resolve ambiguity into a single confident-sounding answer.

---

## 🏆 Achievements

- A working agent loop that genuinely decides its own tool usage, not a hardcoded if/else dressed up as an agent
- A full plan → execute → synthesize research pipeline, going from one vague question to a structured, sourced report
- Built-in safeguards against three of agentic AI's most common failure modes: infinite loops, tool crashes, and fabricated citations
- 25 tests covering tools, the agent loop's tool-selection behavior, and the research pipeline
- A Research Depth control that makes the cost/thoroughness tradeoff an explicit, user-facing setting rather than a hidden constant

---

## 🔭 Next Week Preview

Week 5 deliberately stays single-agent — understanding where one agent's capabilities end is what makes the reasoning behind multi-agent systems (later in Phase 2) actually click, rather than just chaining several LLM calls together without understanding why more than one agent is needed. Refer to the roadmap for the Week 6 repository name and topics once finalized.

---

## 📂 Git Commit

```bash
git add .
git commit -m "docs: add week 5 summary"
git push
```
