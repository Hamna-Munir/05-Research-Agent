# Engineering Journal — Week 05

Daily engineering log for the AI Research Agent (Days 29–35). Not a personal diary — a record of what was built, what design decisions were made, and what would be done differently.

**Note:** these entries are written from the build/design process. Real runtime results (from actually running the app and evaluation set) should be added once testing is complete — see the "To Verify" note at the end of each relevant entry.

---

## Day 29

**Today**
Built the core agent loop (`agent.py`) and the first 5 tools (`add`, `subtract`, `multiply`, `divide`, `calculate_percentage`) in `tools.py`. The loop follows Goal → Think/Decide → Action → Tool → Observation → Decide Again → Final Answer, using the LLM's native tool-calling API rather than manually parsing text for intent.

**Biggest Problem**
Deciding how strict to be about error handling in the calculator tools themselves — a naive `divide()` would raise a `ZeroDivisionError` and crash the whole agent loop over one bad input.

**How I Solved It**
Every tool returns an error *string* on failure (e.g., "Error: cannot divide by zero.") instead of raising an exception — the LLM can read that string and respond to the user appropriately, rather than the whole process dying.

**What I Would Improve / To Verify**
Need to actually run the calculator agent against a range of math questions to confirm the LLM reliably picks tools instead of doing arithmetic "in its head" (a known common error for this exact setup, per the Day 29 curriculum notes).

---

## Day 30

**Today**
Formalized tool calling with proper JSON schemas (`TOOL_SCHEMAS`) and added 3 utility tools: `get_current_date`, `calculate` (folded into the calculator tools), and `word_count`. Built `execute_tool()` as a single safe entry point for running any tool by name.

**Biggest Problem**
Making sure tool schema parameter names exactly match the actual Python function parameter names — a mismatch here would mean the LLM calls a tool correctly, but `execute_tool()` passes arguments the function doesn't recognize, causing a silent failure.

**How I Solved It**
Wrote schemas and functions side-by-side in `tools.py` rather than in separate files, so any drift between a schema's parameter and a function's actual signature is visually obvious while writing them.

**What I Would Improve / To Verify**
Should write a test that specifically checks every tool schema's parameter names against its corresponding function's real signature, rather than relying on manual visual consistency — this is exactly the kind of mismatch that's easy to introduce later when adding tool #9 or #10.

---

## Day 31

**Today**
Added `web_search()` using DuckDuckGo (no API key required), and built `execute_subtask()` in `researcher.py` to run a search, summarize the results, and — critically — keep the source URLs attached to the summary rather than discarding them.

**Biggest Problem**
Deciding what should happen when the search itself fails (network issue, rate limit, etc.) versus when the search succeeds but returns nothing useful — these are different failure modes that call for different handling.

**How I Solved It**
`web_search()` returns a list with an `"error"` key on failure, and `execute_subtask()` checks for that specifically, versus a separate check for an empty (but successful) results list — so a research report can eventually say "search failed" versus "no information found," which are genuinely different findings.

**What I Would Improve / To Verify**
Need to run this against a real, deliberately obscure query to see what "no results" actually looks like in practice from DuckDuckGo's API, since the current handling is based on anticipated failure modes rather than an observed one.

---

## Day 32

**Today**
Built `planner.py`'s `create_research_plan()`, which prompts the LLM to break a research question into 5-7 subtasks and parses the numbered-list response into a Python list.

**Biggest Problem**
LLM output for "give me a numbered list" isn't perfectly guaranteed to come back as a clean `1. ... 2. ...` format every time — formatting could drift (bullets instead of numbers, extra preamble text, etc.).

**How I Solved It**
Wrote `_parse_numbered_list()` with a regex that specifically looks for the `N.` or `N)` pattern, and added a fallback: if no numbered lines are found at all, treat the entire response as one single subtask rather than returning an empty list and silently breaking the rest of the pipeline.

**What I Would Improve / To Verify**
Should test this parser against a handful of real LLM responses (not just the ideal-case example) to see how often the fallback path actually triggers — that failure rate would tell me whether the parsing approach needs to be more robust (e.g., asking for JSON output instead of a numbered list).

---

## Day 33

**Today**
Wrote the synthesis system prompt (`SYNTHESIS_SYSTEM_PROMPT`) requiring a strict report structure (Executive Summary, Key Findings, Evidence, Sources, Limitations, Recommendation) and explicit instructions to never invent sources and to present disagreement between sources honestly rather than blending it away.

**Biggest Problem**
Nothing in the code itself *guarantees* the model won't invent a source — a prompt instruction is a strong nudge, not a hard constraint, unlike the deterministic checks used elsewhere in the pipeline (e.g., tool schema validation).

**How I Solved It**
Added `has_sources()` in `evaluator.py` as a lightweight cross-check: it verifies that URLs mentioned in the final report actually match URLs that were genuinely retrieved during the research phase. This doesn't catch every possible fabrication, but it catches the most obvious case — a source appearing in the report that was never in the findings at all.

**What I Would Improve / To Verify**
This check is fairly basic (string matching against retrieved URLs). Once real reports are generated, I should manually read a handful of them and confirm no subtler fabrication slipped through — e.g., a real source misquoted to say something it didn't actually say.

---

## Day 34

**Today**
Built `evaluator.py` with automatic checks (`has_sources`, `addresses_question`, `has_required_sections`) meant to support — not replace — a manual evaluation.csv process across 15+ questions spanning easy, complex, edge-case, and unanswerable categories.

**Biggest Problem**
`addresses_question()` uses simple keyword overlap between the question and the report, which is a weak relevance signal — Week 4's lesson (semantic similarity beats keyword matching) directly applies here, but bringing in embeddings for this one lightweight check felt like overkill for a fast automatic screen.

**How I Solved It**
Kept the keyword-overlap check as a coarse first-pass filter — good enough to catch a report that's wildly off-topic — while relying on the *manual* evaluation.csv process (Day 34's actual core exercise) to catch subtler relevance issues that keyword matching would miss.

**What I Would Improve / To Verify**
Still need to actually build `data/evaluation.csv` with 15 real questions and run the full agent against every one of them, recording genuine pass/fail results — this is the one piece of Week 5 that can't be verified through code review alone; it requires actually running the system end-to-end and being honest about where it fails.

---

## Day 35

**Today**
Connected every piece into `app.py` — a Streamlit UI with a Research Depth control (Quick/Standard/Deep) that adjusts how many search results are gathered per subtask, plus an expandable view of per-subtask findings and the automatic evaluator checks.

**Biggest Problem**
Balancing "Deep" mode's thoroughness against response time and API cost — more subtasks and more search results per subtask means more sequential LLM and search calls, which could make Deep mode feel slow without any indication of progress.

**How I Solved It**
Added distinct spinner messages for the planning stage and the research stage separately (rather than one generic "loading..." for the entire pipeline), so the user has some sense of which stage is currently running even during a longer Deep-mode request.

**What I Would Improve / To Verify**
Haven't yet measured actual wall-clock time for Quick vs Standard vs Deep on a real question — that would tell me whether Deep mode needs a stronger warning about expected wait time, or whether a progress indicator per-subtask (rather than one spinner for the whole research phase) would be worth the added complexity.

---

## Week 05 — Overall Reflection

This week's projects (and journal entries) look different from Weeks 2–4's: the earlier weeks' journals recorded bugs *found through actually running the code* — wrong model names, CSS rendering issues, an incorrect similarity metric caught by inspecting real output. This week's entries instead record engineering decisions made *while designing* the code — error handling strategy, fallback parsing, fabrication guards — because the natural next step, not yet done, is to actually run the full agent against Day 34's 15-question evaluation set and update this journal with what genuinely breaks. An agent is exactly the kind of system where design intentions and real behavior can diverge the most — which makes that upcoming evaluation step the one that will teach the most, same as it did in every previous week.
