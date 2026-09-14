"""
evaluator.py
Day 34 — automatic checks that support (not replace) manual evaluation
against evaluation.csv. These are the bonus-challenge checks: does the
answer contain sources, does it address the question, does it contain
unsupported claims.
"""


def has_sources(report: str, findings: list[dict]) -> bool:
    """Checks whether the report actually references real retrieved sources."""
    all_sources = [url for f in findings for url in f.get("sources", [])]
    if not all_sources:
        return False
    return "## Sources" in report or any(url in report for url in all_sources)


def addresses_question(report: str, research_question: str) -> bool:
    """
    Very basic relevance check: does the report share meaningful keyword
    overlap with the question? (A real system would use semantic
    similarity — see Week 4 — but this keeps the evaluator dependency-free.)
    """
    question_words = set(w.lower() for w in research_question.split() if len(w) > 3)
    report_lower = report.lower()
    matches = sum(1 for w in question_words if w in report_lower)
    return matches >= max(1, len(question_words) // 3)


def has_required_sections(report: str) -> bool:
    """Confirms the structured report format (Day 33) was actually followed."""
    required = ["Executive Summary", "Key Findings", "Sources", "Limitations", "Recommendation"]
    return all(section in report for section in required)


def evaluate_report(research_question: str, report: str, findings: list[dict]) -> dict:
    """
    Runs all automatic checks and returns a summary dict — meant to
    support the manual evaluation.csv process (Day 34), not replace it.
    """
    return {
        "has_sources": has_sources(report, findings),
        "addresses_question": addresses_question(report, research_question),
        "has_required_sections": has_required_sections(report),
    }
