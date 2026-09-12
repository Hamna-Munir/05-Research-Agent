# Day 34 — Research Agent Evaluation

**Objective:** Test whether the agent is actually reliable — not just whether it runs without crashing.

---

## 📖 Theory

### Agent evaluation

Building an agent isn't the same as knowing it works well. Evaluation means systematically testing the agent against a range of realistic (and deliberately difficult) questions, then judging the results against clear criteria — the same evaluation discipline established in Week 2 (Day 13), Week 3 (Day 20), and Week 4 (Day 27), now applied to an agent instead of a single prompt.

### Evaluation criteria for an agent

- **Accuracy** — is the final answer factually correct given the evidence gathered?
- **Relevance** — does the answer actually address the question asked?
- **Completeness** — does the answer cover the key aspects of the question, or is it missing obvious parts?
- **Citation quality** — are sources actually present, and do they genuinely support the claims made?
- **Tool-use errors** — did the agent call the right tools, with correct arguments, without crashing?

### Failure cases and edge cases

A failure case is a question where the agent's output is clearly wrong or unhelpful. An edge case is a scenario that's unusual but plausible — a very vague query, an oddly specific question, or a topic the agent has very little information about.

### Creating an evaluation dataset

At least 15 test questions, spanning 4 categories:

- **5 Easy** — clear, direct questions with a well-defined answer (e.g., "What is RAG?")
- **5 Complex** — multi-part or comparative questions (e.g., "Compare RAG and fine-tuning.")
- **3 Edge Cases** — vague or unusually phrased queries (e.g., "Give me information about X from a very vague query.")
- **2 Unanswerable** — questions with no knowable answer (e.g., "What will AI agents definitely look like in 2040?")

---

## 🎥 Best Resource

Search: "LLM Agent Evaluation Tutorial"

---

## 💻 Coding Exercise

Create `evaluation.csv` with these columns:

| question | expected_behavior | agent_answer | source_quality | answer_quality | passed | notes |
|---|---|---|---|---|---|---|

---

## 🛠 Mini Project

Run the Research Agent against all 15+ questions and calculate:

- **Tool Success Rate** — % of tool calls that executed without error
- **Answer Quality** — subjective 1-5 rating per question, or pass/fail against expected behavior
- **Source Quality** — were real, relevant sources included?
- **Failure Rate** — % of questions where the agent's output was clearly wrong or unhelpful

---

## 🧠 Quiz

1. Why is evaluation necessary even after the agent appears to work on a few examples?
2. What's the difference between an edge case and an unanswerable question?
3. What counts as a "tool failure," specifically?
4. When should the agent say "I don't know" instead of producing a confident-sounding answer?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus Challenge

Add an automatic evaluator that checks, for each answer:

- Does the answer contain sources?
- Does the answer actually address the question asked?
- Does the answer contain claims that aren't backed by any retrieved evidence?

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Only testing successful examples | Confirmation bias — running the questions most likely to work well | Deliberately include hard, vague, and unanswerable questions in the evaluation set |
| Skipping edge cases | They're harder to write and evaluate than easy questions | Budget explicit time for edge cases; they usually reveal the most useful failures |
| Skipping human evaluation entirely | Relying only on automated pass/fail checks that miss subtle quality issues | Manually read through at least the failed and borderline cases |
| Treating "it works on my example" as proof of quality | One successful run doesn't represent overall reliability | Always evaluate against the full dataset, not a single anecdotal test |

---

## ✅ Checklist

- [ ] 15+ test questions written
- [ ] Easy cases tested
- [ ] Complex cases tested
- [ ] Edge cases tested
- [ ] Unanswerable cases tested
- [ ] Evaluation table filled in with real results
- [ ] Failure analysis documented
- [ ] Git commit made

---

## 📂 GitHub Push

```bash
git add .
git commit -m "test: evaluate research agent reliability"
git push
```

---

## 📝 Journal

*Most important question: What did my agent fail at?*

*Failures should not be hidden — they are part of your engineering learning.*

---

## ⭐ Daily Skill Learned

AI Agent Evaluation + Reliability Testing
