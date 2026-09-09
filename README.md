<p align="center">
  <img src="assets/banner.svg?v=2" alt="AI Research Agent Banner" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Tool%20Calling-Function%20Schemas-14b8a6?style=flat-square" alt="Tool Calling"/>
  <img src="https://img.shields.io/badge/Agent-Task%20Decomposition-38bdf8?style=flat-square" alt="Agent"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Status-In%20Progress-f59e0b?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/Last%20Commit-Week%205-14b8a6?style=flat-square" alt="Last Commit"/>
</p>

<p align="center">
  An AI agent that plans research, decides which tools to call, gathers evidence, evaluates source reliability, and produces a structured report.<br/>
  Fifth deliverable of a <b>90-day AI Engineering roadmap</b> (Phase 1: Foundation, Week 5).
</p>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#️-installation)
- [How to Run](#️-how-to-run)
- [Architecture](#️-architecture)
- [Agent vs Chatbot](#-agent-vs-chatbot)
- [Folder Structure](#-folder-structure)
- [Future Improvements](#-future-improvements)
- [Roadmap Context](#-roadmap-context)
- [Author](#-author)
- [License](#-license)

---

## 📖 Overview

**AI Research Agent** is the first project in this roadmap that goes beyond a normal LLM application: instead of just answering a question directly, it receives a goal, decides which tools it needs, breaks a complex research question into smaller subtasks, gathers information using those tools, evaluates the reliability of what it finds, and synthesizes everything into a structured research report — citing its sources rather than asserting conclusions from nowhere.

This is **Repo 5 of 10+** in a structured 90-day AI Engineering roadmap, moving from LLM fundamentals → agentic systems → deployable AI products. This week specifically builds the **single-agent foundation** — the reasoning for why multi-agent systems (Phase 2) are needed later will make a lot more sense after working through the limits of one agent first.

---

## ✨ Features

- 🧮 **Tool Calling** — the agent decides which function to call (calculator, search, word count, etc.) rather than the developer hardcoding the logic path
- 🧩 **Task Decomposition** — a complex research question is broken into smaller, sequential subtasks before execution
- 🔍 **Search Integration** — the agent generates its own search queries and gathers information rather than relying only on training knowledge
- 📊 **Source Analysis** — findings are linked to evidence and a reliability assessment, not presented as unattributed fact
- ⚠️ **Handles Disagreement & Uncertainty** — when sources conflict, the agent presents both views instead of inventing a single answer
- 📄 **Structured Research Reports** — Executive Summary, Key Findings, Evidence, Sources, Limitations, Recommendation
- 🧪 **Evaluated against 15+ test questions** — easy, complex, edge-case, and genuinely unanswerable questions
- ⚡ **Research Depth control** — Quick / Standard / Deep, trading off search count against thoroughness

---

## 🎥 Demo

*(Add a screenshot or short GIF/video here once available)*

```
assets/screenshots/
```

---

## 🛠️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/Hamna-Munir/05-Research-Agent.git
cd 05-Research-Agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then add your API key(s)
```

---

## ▶️ How to Run

```bash
streamlit run src/app.py
```

Once running, open the local URL Streamlit prints, enter a research question, and watch the agent plan, search, and report back with sources.

---

## 🏗️ Architecture

```
                USER
                  ↓
          Research Question
                  ↓
          ┌───────────────┐
          │ Research Agent│
          └───────┬───────┘
                  ↓
          Task Decomposition
                  ↓
        ┌─────────┴─────────┐
        ↓                   ↓
   Search Tool          Other Tools
        ↓                   ↓
        └─────────┬─────────┘
                  ↓
          Information Gather
                  ↓
          Source Analysis
                  ↓
            AI Synthesis
                  ↓
          Research Report
```

The core agent loop underlying every tool decision:

```
Goal → Think/Decide → Action → Tool → Observation → Decide Again → Final Answer
```

---

## 🤖 Agent vs Chatbot

A regular chatbot receives a message and generates a response — a single, direct step. This Research Agent is fundamentally different: it receives a **goal**, decides **which tools it needs** (rather than the developer hardcoding that decision), breaks the goal into **subtasks**, executes multiple steps in sequence, and only produces a final answer once it has gathered and evaluated evidence. The agent's behavior isn't fully predetermined by the code path — it's decided dynamically based on the specific question asked.

---

## 📂 Folder Structure

```
05-Research-Agent/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── .env.example
│
├── docs/
│   └── week-05-summary.md
│
├── notes/
│   ├── day-29.md
│   ├── day-30.md
│   ├── day-31.md
│   ├── day-32.md
│   ├── day-33.md
│   ├── day-34.md
│   └── day-35.md
│
├── assets/
│   ├── banner.svg
│   └── screenshots/
│
├── data/
│   └── evaluation.csv
│
├── tests/
│   ├── test_tools.py
│   ├── test_agent.py
│   └── test_research.py
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── agent.py
│   ├── tools.py
│   ├── planner.py
│   ├── researcher.py
│   ├── evaluator.py
│   ├── prompts.py
│   └── config.py
│
└── journal.md
```

---

## 🚀 Future Improvements

- [ ] Add a real web search API (this week's search tool is intentionally simple)
- [ ] Add citation-level fact-checking against multiple independent sources
- [ ] Persist research sessions so a report can be revisited later
- [ ] Add streaming output so the agent's reasoning steps are visible in real time
- [ ] Move toward multi-agent specialization (Phase 2 preview)

---

## 🧭 Roadmap Context

This project is **Week 5 of Phase 1** in a 90-day AI Engineering roadmap:

| Phase | Focus | Days |
|---|---|---|
| Phase 1 | Foundation — Personal Assistant → Writing Assistant → PDF Assistant → Knowledge Assistant → Research Agent | 1–30 |
| Phase 2 | Agent Engineering — RAG, LangGraph, MCP | 31–60 |
| Phase 3 | Business AI Systems — Multi-Agent, Deployment | 61–90 |

---

## 👩‍💻 Author

**Hamna Munir**
Software Engineering & AI/ML Student | Building deployable AI/ML projects

- GitHub: [@Hamna-Munir](https://github.com/Hamna-Munir)
- Hugging Face: [@Hamna27](https://huggingface.co/Hamna27)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
