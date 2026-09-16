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

---

## Post-Ship Audit — Reliability, Search Quality & Report Completeness

**Today**
Ran a structured audit against 4 real questions (customer support, a 2040 forecast, tool calling, and RAG) and fixed what the testing actually revealed:
1. **Reliability** — wrapped the planner, researcher, and synthesis LLM calls in try/except so a failed API call returns a graceful fallback instead of crashing; wrapped the Streamlit app's research flow in try/except so a raw traceback is never shown to the user.
2. **Report truncation** — the Recommendation section was getting cut off because `max_tokens` for synthesis was 1200. Increased to 2500 and added a repair step: if any of the 6 required sections is still missing after generation, one follow-up call asks specifically for the missing section(s) rather than shipping an incomplete report.
3. **Search-quality filtering** — added `_filter_and_dedupe()` to drop duplicate-domain results and results with zero keyword overlap with the subtask (fixed the earlier "RAG" search returning Diffchecker-style document-comparison tools).
4. **A "Tool (band)" false positive** — the keyword filter still let through a Wikipedia article about the rock band "Tool" for a "tool calling" subtask, since "tool" literally overlaps even though the meaning doesn't. Added a small exclusion list (band/album/lyrics/etc.) as a targeted, proportionate fix — not a full semantic filter, which would be out of scope.
5. **A separate, unrelated theme bug** — text inside expanders was rendering nearly invisible (white-on-white) because Streamlit's dark-theme default was active (matching the browser/OS dark mode) and overriding the app's light-theme text color for un-styled `st.write()` content. Fixed with an explicit `.streamlit/config.toml` forcing light theme, plus CSS forcing text color inside expanders regardless of theme.

**Biggest Problem**
After all of the above, re-testing revealed the dominant remaining issue isn't code at all: DuckDuckGo's free search backend rate-limits heavily under repeated testing (3-4 of 5 subtasks failing outright in a single research run), and occasionally returns genuinely irrelevant results for niche or forward-looking queries (a printable-ruler website and an unrelated leaked-document archive both surfaced for a "2040 AI agents" query) — noise the search engine itself introduced, which no amount of downstream filtering can correct, since there was nothing relevant in the result set to select from.

**How I Solved It**
Recognized this as a genuine infrastructure ceiling, not a bug to keep patching. Continuing to add filtering rules would have been chasing symptoms of a free search library that's fundamentally rate-limited and occasionally low-quality — the honest fix is a paid search API (Tavily, SerpAPI, Bing Search API), which was a deliberate decision NOT to add in v1.0, to keep the project free to run. Documented this explicitly in the README's new "Known Limitations" section instead of leaving it as an implied gap or continuing to add speculative code fixes that testing wouldn't actually validate.

**What I Would Improve**
If reliability mattered more than staying free-tier (e.g., an actual production deployment), swapping in a paid search API would resolve both the rate-limiting and the occasional garbage-result problem in one change, since paid providers maintain higher-quality, less-restricted indexes. For this portfolio project, the more valuable lesson was learning to recognize when a problem has moved from "my code" to "the tool my code depends on" — and that documenting a known limitation honestly is better engineering than quietly patching around it with diminishing returns.

---

## Week 05 — Overall Reflection

This week's journal ended up in two parts, and that split is itself worth noting. The first pass (Days 29-35) recorded design decisions made *while building* — error handling strategy, fallback parsing, fabrication guards — because the code hadn't been run against real questions yet. The second pass (the post-ship audit) recorded what *actually broke* once it was: an empty search query from a token-budget mistake, a rate-limited search backend, a truncated report section, a keyword filter with a literal-but-wrong match, and an invisible-text theme bug. Every one of those was invisible from reading the code — they only surfaced by running real questions and looking closely at real output, the same lesson Weeks 2, 3, and 4 each taught in their own way. The genuinely new lesson this week was knowing when to stop patching: once the dominant failure mode became "the free search engine itself returned bad results," no further code change inside this project could fix that — the honest move was documenting it as a known limitation rather than chasing it with increasingly specific rules.
