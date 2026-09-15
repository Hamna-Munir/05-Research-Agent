"""
researcher.py
Day 31 -> execute_subtask(): runs a web search for one subtask and
           summarizes the results, preserving sources.
Day 33 -> source tracking carried through to synthesis; disagreement
           between sources is preserved rather than blended away.
Day 32/33 -> synthesize_report(): combines all subtask findings into
              the final structured research report.
"""

from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL
from src.tools import web_search
from src.prompts import SYNTHESIS_SYSTEM_PROMPT, build_synthesis_prompt

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def generate_search_query(subtask: str) -> str:
    """
    Day 31 fix — converts a verbose, instructional subtask (e.g.
    "Define the acronym 'RAG' and identify its full form(s) in various
    contexts") into a short, search-engine-friendly query (e.g.
    "RAG acronym meaning AI"). Without this step, the raw subtask
    sentence was being sent directly to the search tool, and its
    stray instructional words (e.g. "identify", "compare") were
    matching unrelated results instead of the actual topic.

    Args:
        subtask: the research subtask from planner.py.

    Returns:
        A short (3-8 word) search query. Falls back to a simple
        heuristic-shortened version of the subtask if the LLM call
        returns nothing usable.
    """
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": (
                f"Convert this research subtask into a short, specific web "
                f"search query (3-8 words, no instructional phrasing like "
                f"'define' or 'identify'). Return ONLY the query, nothing else.\n\n"
                f"Subtask: {subtask}"
            ),
        }],
        temperature=0.1,
        max_tokens=150,  # reasoning models (e.g. gpt-oss) use tokens for
                         # internal reasoning before the visible answer —
                         # 30 was too low and produced empty content every time
    )
    query = (response.choices[0].message.content or "").strip().strip('"')

    if query:
        return query

    # Fallback: strip common instructional verbs and take the first few
    # meaningful words, rather than sending an empty query to the search tool
    return _fallback_query(subtask)


def _fallback_query(subtask: str) -> str:
    """Simple heuristic fallback if the LLM query-generation call fails."""
    stop_prefixes = [
        "define", "identify", "explain", "describe", "summarize", "compare",
        "analyze", "evaluate", "assess", "investigate", "conduct", "discuss",
        "the", "and", "or", "of", "for", "with", "a", "an",
    ]
    words = [w for w in subtask.replace(",", " ").split() if w.lower().strip(".:;") not in stop_prefixes]
    return " ".join(words[:8]) if words else subtask[:60]


def _filter_and_dedupe(results: list[dict], subtask: str, search_query: str) -> list[dict]:
    """
    Search-quality filter: removes duplicate-domain results and rejects
    results that don't meaningfully relate to the subtask.

    Fix (this round): the previous version had a loop bug where the
    "keep at least one result" fallback was checked INSIDE the loop
    (`not filtered`), which meant the very first result processed was
    always kept regardless of relevance, since `filtered` starts empty.
    This is exactly why fully unrelated results (printable-ruler.net,
    Wikileaks Vault 7, toolband.com) were slipping through — they just
    happened to be first in the list. The fallback now only applies
    after ALL results have been checked, and per the current
    requirement, there IS no keep-anything fallback anymore: if
    nothing is genuinely relevant, this returns an empty list, and
    execute_subtask reports "insufficient relevant evidence" instead
    of citing an unrelated source.

    Relevance is judged by keyword overlap with BOTH the original
    subtask and the generated search query, requiring a meaningful
    fraction of words to match (not just one incidental word like
    "tool" matching a band name) — plus a small exclusion list for
    common obvious false-positive categories.
    """
    query_words = set(w.lower() for w in (subtask + " " + search_query).split() if len(w) > 3)
    # Require at least half the meaningful words to appear (min 2),
    # so a single incidental word match (e.g. "tool") isn't enough.
    min_overlap = max(2, len(query_words) // 2)

    OFF_TOPIC_SIGNALS = [
        "band", "album", "lyrics", "song", "discography", "music video",
        "tour dates", "setlist", "ticket presale", "fan club",
    ]

    seen_domains = set()
    filtered = []
    for r in results:
        domain = r["url"].split("/")[2] if r.get("url") and "//" in r["url"] else r.get("url", "")
        if domain in seen_domains:
            continue

        text = (r.get("title", "") + " " + r.get("snippet", "")).lower()

        if any(signal in text for signal in OFF_TOPIC_SIGNALS):
            continue

        overlap = sum(1 for w in query_words if w in text)
        if overlap < min_overlap:
            continue  # not relevant enough — reject, no exceptions

        seen_domains.add(domain)
        filtered.append(r)

    return filtered  # empty is a valid, honest outcome now


def execute_subtask(subtask: str, max_results: int = 3) -> dict:
    """
    Runs a web search for one research subtask and summarizes the
    results, keeping source URLs attached to the summary.

    Args:
        subtask: one specific research subtask (from planner.py).
        max_results: how many search results to gather for this subtask.

    Returns:
        A dict with 'subtask', 'summary', and 'sources' (list of URLs).
    """
    search_query = generate_search_query(subtask)
    results = web_search(search_query, max_results=max_results)

    if results and "error" in results[0]:
        return {"subtask": subtask, "search_query": search_query, "summary": f"Search failed: {results[0]['error']}", "sources": []}

    if not results:
        return {"subtask": subtask, "search_query": search_query, "summary": "No search results found.", "sources": []}

    # Search-quality fix: drop irrelevant/duplicate results before summarizing
    results = _filter_and_dedupe(results, subtask)

    combined_text = "\n\n".join(f"{r['title']}: {r['snippet']}" for r in results)
    sources = [r["url"] for r in results if r.get("url")]

    summary_prompt = (
        f"Summarize the key information relevant to: '{subtask}'\n\n"
        f"Based on these search results:\n{combined_text}\n\n"
        f"Give a concise 2-4 sentence summary, using only this information."
    )

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.2,
            max_tokens=300,
        )
        summary = response.choices[0].message.content or "Could not generate a summary from the search results."
    except Exception as e:
        # Reliability fix: a failed summarization call no longer crashes
        # the whole research run — fall back to the raw search snippets.
        summary = f"(Summary generation failed — showing raw snippets) {combined_text[:400]}"

    return {
        "subtask": subtask,
        "search_query": search_query,
        "summary": summary,
        "sources": sources,
    }


def synthesize_report(research_question: str, findings: list[dict]) -> str:
    """
    Day 32/33 — combines all subtask findings into one structured report,
    citing sources and honestly noting limitations or disagreement.

    Args:
        research_question: the original research question.
        findings: list of dicts from execute_subtask().

    Returns:
        The final structured research report as a string.
    """
    prompt = build_synthesis_prompt(research_question, findings)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2500,  # was 1200 — too low, cutting off the
                              # Recommendation section before it finished
        )
        report = response.choices[0].message.content
        if not report or not report.strip():
            raise ValueError("Empty report returned")
    except Exception as e:
        # Reliability fix: never crash — return a clear, honest fallback
        # instead of letting the Streamlit app show a raw traceback.
        return (
            "## Executive Summary\n"
            "The report could not be generated due to an error contacting "
            "the language model. Please try again.\n\n"
            f"## Limitations\nTechnical error: {str(e)}"
        )

    report = _ensure_required_sections(report, research_question, findings)
    return report


REQUIRED_SECTIONS = [
    "Executive Summary", "Key Findings", "Evidence",
    "Sources", "Limitations", "Recommendation",
]


def _ensure_required_sections(report: str, research_question: str, findings: list[dict]) -> str:
    """
    Report-completeness fix: if the model's response is missing one of
    the 6 required sections (most commonly Recommendation, when the
    response got cut off), make one follow-up call asking only for the
    missing section(s) and append it — rather than shipping an
    incomplete report silently.
    """
    missing = [s for s in REQUIRED_SECTIONS if s not in report]
    if not missing:
        return report

    try:
        repair_prompt = (
            f"The following research report is missing these required "
            f"sections: {', '.join(missing)}.\n\n"
            f"Research question: {research_question}\n\n"
            f"Existing report:\n{report}\n\n"
            f"Write ONLY the missing section(s) now, each starting with "
            f"'## SectionName'. If there isn't enough evidence for a "
            f"section, state that explicitly rather than leaving it blank."
        )
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": repair_prompt}],
            temperature=0.3,
            max_tokens=800,
        )
        addition = response.choices[0].message.content
        if addition and addition.strip():
            return report + "\n\n" + addition
    except Exception:
        pass  # if the repair call also fails, ship the original report as-is

    return report


def run_research(research_question: str, subtasks: list[str], depth_results: int = 3) -> dict:
    """
    Full research pipeline: executes every subtask, then synthesizes
    a final report from all the findings.

    Args:
        research_question: the original question.
        subtasks: list of subtasks from planner.create_research_plan().
        depth_results: how many search results per subtask (Research Depth control).

    Returns:
        A dict with 'report' (final text) and 'findings' (per-subtask detail).
    """
    import time

    findings = []
    for i, subtask in enumerate(subtasks):
        findings.append(execute_subtask(subtask, max_results=depth_results))
        if i < len(subtasks) - 1:
            time.sleep(1)  # small gap between searches — reduces rate-limiting

    report = synthesize_report(research_question, findings)
    return {"report": report, "findings": findings}
