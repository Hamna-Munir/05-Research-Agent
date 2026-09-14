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

    combined_text = "\n\n".join(f"{r['title']}: {r['snippet']}" for r in results)
    sources = [r["url"] for r in results if r.get("url")]

    summary_prompt = (
        f"Summarize the key information relevant to: '{subtask}'\n\n"
        f"Based on these search results:\n{combined_text}\n\n"
        f"Give a concise 2-4 sentence summary, using only this information."
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    return {
        "subtask": subtask,
        "search_query": search_query,
        "summary": response.choices[0].message.content,
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

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1200,
    )

    return response.choices[0].message.content


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
    findings = [execute_subtask(subtask, max_results=depth_results) for subtask in subtasks]
    report = synthesize_report(research_question, findings)
    return {"report": report, "findings": findings}
