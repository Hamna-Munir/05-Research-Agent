# Day 31 — Agent + Search

**Objective:** Teach the agent to retrieve information from outside its own training knowledge. This is where the actual Research Agent begins.

---

## 📖 Theory

### Search tools

A search tool gives the agent a way to look up current or specific information it doesn't already have — instead of answering purely from what the model learned during training (which has a knowledge cutoff and no awareness of anything after it).

### Information retrieval

Information retrieval is the general process of finding relevant information from an external source, given a query. For a research agent, this typically means: generate a search query, run the search, and extract the results worth using.

### Query generation

The agent doesn't just reuse the user's exact question as the search query — it often needs to generate a more effective search query itself. A vague or overly conversational question ("What's going on with AI agents lately?") may need to become a more targeted query ("recent developments AI agents 2026") to get useful results.

### Search → Results → Relevant Information

```
Research Question
       ↓
Generate Search Query
       ↓
Search Tool
       ↓
Search Results
       ↓
Relevant Information
```

Raw search results are rarely the final answer — they need to be read, filtered, and summarized. Not every result is equally relevant, and pulling in low-quality or off-topic results makes the agent's final answer worse, not better.

### Search result parsing

Search results usually come back as a list of items (title, snippet, URL). Parsing means extracting the useful text content from that structure so it can be reasoned about — not just dumping raw search API output into the final answer.

### Relevant information selection

Not every returned result is useful. Part of the agent's job is judging which results actually relate to the question — this is a preview of Day 33's deeper focus on source reliability.

---

## 🎥 Best Resource

Search: "AI Agent Web Search Tool Calling Tutorial"

---

## 💻 Coding Exercise

Give the agent a search tool:

```
Question:
What are the recent trends in AI agents?

Agent
↓
Search
↓
Collect results
↓
Summarize
```

---

## 🛠 Mini Project — Search & Summarize Agent

**Input:**
> "Explain current trends in AI agents."

**Output:**
- Summary
- Key Findings
- Sources

---

## 🧠 Quiz

1. What problem does a search tool solve that the LLM's own training knowledge can't?
2. Why might the agent generate a different search query than the user's literal question?
3. Why shouldn't the first search result be treated as automatically correct?
4. What does "relevant information selection" mean in this context?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus Challenge

Have the agent run **multiple searches** for one research question instead of just one — for example, for "AI agents":

```
AI agents
AI agent frameworks
AI agent applications
```

Then combine the results from all three searches before summarizing.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Blindly trusting the first search result | No filtering/judgment step before using a result | Explicitly instruct the agent (or add logic) to consider multiple results, not just the top one |
| Search query too vague | Passing the user's raw question directly as the query without refining it | Have the agent (or a prompt step) generate a more specific search query first |
| Duplicate information | Multiple search results say the same thing, inflating the "evidence" without adding value | Deduplicate or note when several sources agree, rather than listing the same fact repeatedly |
| Sources not preserved | Search results are summarized but the original source/URL is discarded | Keep source metadata attached to every piece of information carried through the pipeline |

---

## ✅ Checklist

- [ ] Search tool built
- [ ] Search query generation implemented
- [ ] Search results parsed
- [ ] Summarization working
- [ ] Sources included in output
- [ ] Git commit made

---

## 📂 GitHub Push

```bash
git add .
git commit -m "feat: add search capability"
git push
```

---

## 📝 Journal

*Write: How did giving the LLM a search tool change the capabilities of my application?*

---

## ⭐ Daily Skill Learned

Information Retrieval + Search Tool Integration
