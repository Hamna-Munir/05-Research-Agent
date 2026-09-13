# Day 35 — Build, Polish & Deploy

**Objective:** Combine everything from this week into a shipped, portfolio-ready Research Agent v1.0.

---

## 📖 Overview

This is the wrap-up day for Week 5. Nothing new is learned conceptually — instead, everything from Day 29–34 gets connected, polished, tested end-to-end, and shipped.

### Final Architecture

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

---

## 📖 Theory — Review (30 min)

No new tutorial today — review previous notes and code instead. Confirm you can explain, without looking:

- Agent architecture
- Tool calling
- Planning
- Search
- Evidence
- Evaluation
- Error handling

---

## 💻 Final Coding

Complete the full repository structure:

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

## 🛠 Final Project Features — Checklist

- [ ] Research question input
- [ ] Agent planning
- [ ] Task decomposition
- [ ] Search/tool calling
- [ ] Information collection
- [ ] Source tracking
- [ ] Evidence-based synthesis
- [ ] Structured final report
- [ ] Error handling
- [ ] Evaluation
- [ ] Clean UI
- [ ] README
- [ ] Screenshots
- [ ] Deployment

---

## 🧠 Final Quiz — Without Looking at Notes

1. What is an AI agent?
2. What is tool calling?
3. What is an agent loop?
4. How does an agent search for information?
5. What is task decomposition?
6. Why do sources matter?
7. How do you evaluate an agent?
8. When should an agent refuse to answer?
9. What's the difference between an agent and a chatbot?
10. What part of your Research Agent is most likely to fail?

---

## ⭐ Bonus Challenge — Research Depth Option

Add a Research Depth setting:

| Depth | Searches |
|---|---|
| Quick | 2 searches |
| Standard | 5 searches |
| Deep | 8–10 searches |

---

## 🐞 Common Errors (Full-Project Review)

| Error | Likely Cause | Fix |
|---|---|---|
| API key exposed on GitHub | `.env` accidentally committed | Confirm `.gitignore` excludes `.env`; rotate the key if it was ever pushed |
| Infinite agent loop | No stopping condition on the agent's think/act cycle | Add a maximum iteration limit to the agent loop |
| Too many tool calls | No cap on searches/tool usage per question | Respect the Research Depth setting; add a hard upper limit regardless |
| No timeout | A slow tool call (e.g., search) can hang indefinitely | Add timeouts to all external calls |
| No error handling | Any single tool failure crashes the whole agent | Wrap every tool call in error handling (Day 30) |
| Unstructured output | Final report doesn't follow the agreed format | Enforce the structured report template (Day 33) in the synthesis prompt |
| Missing sources | Claims appear without any linked evidence | Require claim-evidence-source structure in synthesis (Day 33) |
| Fake citations | Model invents a source that was never retrieved | Only allow sources that came from an actual tool call into the final report |
| No evaluation | Shipping without running the 15+ question test set | Complete Day 34's evaluation before calling this "done" |

---

## ✅ Final Week Checklist

- [ ] Agent works
- [ ] Tools work
- [ ] Search works
- [ ] Planning works
- [ ] Sources captured
- [ ] Research report generated
- [ ] 15+ evaluation cases tested
- [ ] Errors handled
- [ ] README complete
- [ ] Architecture documented
- [ ] Screenshots added
- [ ] GitHub pushed
- [ ] App deployed
- [ ] Week summary written
- [ ] Journal completed

---

## 📂 GitHub Push

```bash
git add .
git commit -m "feat: ship AI Research Agent v1.0"
git push
```

---

## 📝 Journal — Week 5 Reflection

Write a proper reflection covering:

- What did I build?
- What did I learn about agents?
- Which tool was most useful?
- What failed?
- How did I evaluate the agent?
- What would I improve in a production version?

---

## ⭐ Daily Skill Learned

End-to-End AI Agent Engineering + Deployment

---

## 📊 Week 5 — Skills Progression

```
AI Agent Fundamentals
        ↓
Tool Calling
        ↓
Function Integration
        ↓
Search & Information Retrieval
        ↓
Task Decomposition
        ↓
Agent Planning
        ↓
Source Verification
        ↓
Evidence-Based Generation
        ↓
Agent Evaluation
        ↓
Deployment
```

By the end of Week 5, this should be explainable clearly:

> "I can build a single AI agent that receives a goal, decides which tools it needs, breaks complex tasks into smaller steps, gathers information, analyzes evidence, and produces a structured result."

**Note:** Week 5 is deliberately single-agent, not multi-agent. Understanding the limits of one agent first is what makes the reasoning behind multi-agent systems (later in the roadmap) actually click, rather than just connecting several LLM calls together without understanding why.
