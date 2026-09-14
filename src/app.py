"""
app.py
AI Research Agent — Streamlit UI
Developed by Hamna Munir

Full pipeline: research question -> plan -> execute subtasks via search
-> synthesize structured report -> automatic quality checks.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.planner import create_research_plan
from src.researcher import run_research
from src.evaluator import evaluate_report

st.set_page_config(
    page_title="Lumen Research | Hamna Munir",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# GLOBAL STYLE — Clarity-AI-inspired: warm cream/gold canvas, elegant serif
# accent typography, crisp (non-blurred) cards with a subtle glow behind the
# hero only. Cards use Streamlit's native `st.container(key=...)` so their
# CSS class actually wraps the real widgets inside them (no broken div hacks).
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        :root {
            --ink: #2B2620;
            --muted: #837A6B;
            --muted-soft: #A79E8E;
            --gold: #B8892E;
            --green: #4F7A5B;
            --card-bg: #FFFFFF;
            --border: #ECE3D2;
            --bg: #FBF7EF;
            --radius-lg: 22px;
            --radius-md: 14px;
            --radius-sm: 10px;
            --shadow-soft: 0 12px 30px rgba(80, 62, 22, 0.07);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--ink);
        }

        .stApp {
            background-color: var(--bg);
            background-image:
                radial-gradient(circle at 50% 0%, rgba(233, 194, 121, 0.20) 0%, rgba(233, 194, 121, 0) 38%),
                radial-gradient(circle at 92% 10%, rgba(196, 214, 189, 0.18) 0%, rgba(196, 214, 189, 0) 35%);
            background-attachment: fixed;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            max-width: 900px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        em, .accent-serif {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 600;
            color: var(--gold);
        }

        .topnav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 6px 0 6px;
            margin-bottom: 1.4rem;
        }
        .brand { display: flex; align-items: center; gap: 10px; }
        .brand-word {
            font-family: 'Playfair Display', serif;
            font-weight: 600;
            font-size: 1.25rem;
            color: var(--ink);
        }
        .brand-word span { color: var(--gold); font-style: italic; }
        .floating-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--ink);
            box-shadow: var(--shadow-soft);
        }

        .hero-wrap {
            position: relative;
            text-align: center;
            margin: 1.4rem 0 1.8rem 0;
            padding-top: 70px;
        }
        .hero-wrap::before {
            content: "";
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(233,194,121,0.40) 0%, rgba(233,194,121,0) 70%);
            z-index: 0;
        }
        .hero-wrap > * { position: relative; z-index: 1; }
        .logo-mark {
            width: 62px; height: 62px;
            margin: 0 auto 1.1rem auto;
            border-radius: 18px;
            display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, #E9C279 0%, #4F7A5B 130%);
            box-shadow: 0 10px 22px rgba(184, 137, 46, 0.30);
        }
        .hero-title {
            font-size: 2.7rem;
            font-weight: 800;
            letter-spacing: -0.01em;
            line-height: 1.16;
            color: var(--ink);
            margin-bottom: 0.9rem;
        }
        .hero-sub {
            color: var(--muted);
            font-size: 1.04rem;
            max-width: 560px;
            margin: 0 auto;
            line-height: 1.6;
        }

        div[data-testid="column"] .stButton > button {
            border-radius: 999px !important;
            padding: 0.6rem 1.5rem !important;
            font-size: 0.86rem !important;
            border: none !important;
            font-weight: 700 !important;
            width: 100%;
            transition: 0.15s ease;
        }
        .stButton > button[kind="primary"] {
            background: var(--ink) !important;
            color: #FFFFFF !important;
            box-shadow: var(--shadow-soft);
        }
        .stButton > button[kind="primary"]:hover { background: var(--green) !important; }
        .stButton > button[kind="secondary"] {
            background: #F1E9D8 !important;
            color: var(--muted) !important;
            border: 1px solid var(--border) !important;
            box-shadow: none !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background: #E9DDC2 !important;
            color: var(--ink) !important;
        }

        div.st-key-ask_card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-soft);
            padding: 18px 20px 16px 20px;
            margin-top: 0.4rem;
        }
        div.st-key-ask_card div[data-testid="stTextInput"] input {
            background: #FFFFFF !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            font-size: 1rem !important;
            color: var(--ink) !important;
        }
        div.st-key-ask_card div[data-testid="stTextInput"] input::placeholder {
            color: var(--muted-soft) !important;
        }
        div.st-key-ask_card div[data-testid="stTextInput"] input:focus {
            border-color: var(--gold) !important;
            box-shadow: 0 0 0 3px rgba(184,137,46,0.12) !important;
        }
        div.st-key-ask_card div[data-testid="stTextInput"] > div,
        div.st-key-ask_card div[data-testid="stTextInput"] > div > div {
            background: transparent !important;
            border: none !important;
        }
        .ask-hint {
            font-size: 0.82rem;
            color: var(--muted-soft);
            padding-top: 10px;
        }
        div.st-key-ask_card .stButton > button {
            background: var(--ink) !important;
            color: #FFFFFF !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.75rem 1.4rem !important;
            font-weight: 700 !important;
            width: 100%;
            margin-top: 10px;
        }
        div.st-key-ask_card .stButton > button:hover { background: var(--green) !important; }

        .hint-line {
            text-align: center;
            color: var(--muted-soft);
            font-size: 0.85rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }

        .section-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--ink);
            margin: 2.2rem 0 0.9rem 0;
        }
        .section-label .chip {
            background: var(--ink);
            color: white;
            width: 28px; height: 28px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.85rem;
        }

        .plan-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-soft);
            padding: 6px;
        }
        .plan-step {
            display: flex; gap: 12px; align-items: flex-start;
            padding: 12px 14px; font-size: 0.94rem; color: var(--ink);
        }
        .plan-step:not(:last-child) { border-bottom: 1px solid var(--border); }
        .plan-step .num {
            background: #F1E9D8; color: var(--gold); font-weight: 800; font-size: 0.78rem;
            min-width: 22px; height: 22px; border-radius: 6px;
            display: flex; align-items: center; justify-content: center;
        }

        .report-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 30px 32px;
            box-shadow: var(--shadow-soft);
            line-height: 1.65;
            color: var(--ink);
        }
        .report-card h1, .report-card h2, .report-card h3 { color: var(--ink); }
        .report-card * { max-width: 100%; }

        .report-card table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0 1.4rem 0;
            font-size: 0.9rem;
        }
        .report-card th, .report-card td {
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
            overflow-wrap: anywhere;
        }
        .report-card th {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--muted);
            border-bottom: 2px solid var(--border);
            white-space: normal;
        }
        .report-card a {
            color: var(--gold);
            text-decoration: none;
            border-bottom: 1px dotted var(--gold);
            overflow-wrap: anywhere;
        }
        .report-card a:hover { color: var(--green); border-color: var(--green); }

        div[data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            background: var(--card-bg) !important;
            box-shadow: var(--shadow-soft);
            margin-top: 0.9rem;
        }
        div[data-testid="stExpander"] summary { font-weight: 600 !important; }
        div[data-testid="stExpander"] a { overflow-wrap: anywhere; }
        div[data-testid="stAlert"] {
            border-radius: var(--radius-sm) !important;
            border: 1px solid var(--border) !important;
        }

        .search-query-tag {
            display: inline-block;
            background: #F1E9D8;
            color: var(--gold);
            font-family: monospace;
            font-size: 0.78rem;
            padding: 3px 10px;
            border-radius: 999px;
            margin: 4px 0 8px 0;
        }

        .footer-note {
            text-align: center;
            color: var(--muted-soft);
            font-size: 0.82rem;
            margin-top: 3rem;
        }
        .footer-note b { color: var(--ink); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# TOP NAV
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="topnav">
        <div class="brand">
            <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="lg" x1="0" y1="0" x2="34" y2="34" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#E9C279"/>
                        <stop offset="1" stop-color="#4F7A5B"/>
                    </linearGradient>
                </defs>
                <rect width="34" height="34" rx="10" fill="url(#lg)"/>
                <circle cx="14.5" cy="14.5" r="6" stroke="white" stroke-width="2.2"/>
                <line x1="19" y1="19" x2="25" y2="25" stroke="white" stroke-width="2.4" stroke-linecap="round"/>
            </svg>
            <span class="brand-word">Lumen<span> Research</span></span>
        </div>
        <div class="floating-badge">🔗 Built by Hamna Munir</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-wrap">
        <div class="logo-mark">
            <svg width="30" height="30" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="14.5" cy="14.5" r="7" stroke="white" stroke-width="2.4"/>
                <line x1="19.5" y1="19.5" x2="27" y2="27" stroke="white" stroke-width="2.6" stroke-linecap="round"/>
            </svg>
        </div>
        <div class="hero-title">One assistant to streamline<br>your <span class="accent-serif">research</span> workflow.</div>
        <div class="hero-sub">
            Give it a research question — it plans the steps, gathers evidence,
            and writes a structured, source-backed report for you.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# DEPTH SELECTOR
# ----------------------------------------------------------------------------
if "depth_label" not in st.session_state:
    st.session_state.depth_label = "Standard"

seg_cols = st.columns(3, gap="small")
depth_options = ["Quick", "Standard", "Deep"]
for col, label in zip(seg_cols, depth_options):
    with col:
        is_active = st.session_state.depth_label == label
        if st.button(label, key=f"seg_{label}", type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.depth_label = label
            st.rerun()

depth_label = st.session_state.depth_label

# ----------------------------------------------------------------------------
# ASK CARD
# ----------------------------------------------------------------------------
with st.container(key="ask_card"):
    question = st.text_input(
        "Research question",
        placeholder="How can Lumen help with your research today?",
        label_visibility="collapsed",
    )
    col_hint, col_btn = st.columns([2.4, 1])
    with col_hint:
        st.markdown(
            '<div class="ask-hint">📎 Ask anything — we\'ll plan, search, and structure it for you</div>',
            unsafe_allow_html=True,
        )
    with col_btn:
        start_clicked = st.button("Start Research →", use_container_width=True, key="start_btn")

st.markdown(
    '<div class="hint-line">Or try: "Should a startup use AI agents for customer support?"</div>',
    unsafe_allow_html=True,
)

DEPTH_SETTINGS = {"Quick": 2, "Standard": 5, "Deep": 8}
num_subtasks_hint = {"Quick": 2, "Standard": 5, "Deep": 7}

# ----------------------------------------------------------------------------
# RESULTS
# ----------------------------------------------------------------------------
if start_clicked and question.strip():
    with st.spinner("Planning research..."):
        plan = create_research_plan(question)
        plan = plan[: num_subtasks_hint[depth_label]] if depth_label != "Deep" else plan

    st.markdown('<div class="section-label"><span class="chip">🧩</span> Research Plan</div>', unsafe_allow_html=True)
    steps_html = "".join(
        f'<div class="plan-step"><span class="num">{i}</span><span>{subtask}</span></div>'
        for i, subtask in enumerate(plan, start=1)
    )
    st.markdown(f'<div class="plan-card">{steps_html}</div>', unsafe_allow_html=True)

    with st.spinner(f"Researching {len(plan)} subtasks ({depth_label} depth)..."):
        result = run_research(question, plan, depth_results=DEPTH_SETTINGS[depth_label])

    st.markdown('<div class="section-label"><span class="chip">📄</span> Research Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-card">{result["report"]}</div>', unsafe_allow_html=True)

    with st.expander("🔍  Findings per subtask"):
        for finding in result["findings"]:
            st.markdown(f"**{finding['subtask']}**")
            if finding.get("search_query"):
                st.markdown(f'<span class="search-query-tag">🔎 {finding["search_query"]}</span>', unsafe_allow_html=True)
            st.write(finding["summary"])
            if finding["sources"]:
                st.caption("Sources: " + ", ".join(finding["sources"]))
            st.markdown("---")

    with st.expander("✅  Automatic quality checks"):
        checks = evaluate_report(question, result["report"], result["findings"])
        for check, passed in checks.items():
            st.write(f"{'✅' if passed else '⚠️'} {check.replace('_', ' ').title()}")

elif start_clicked and not question.strip():
    st.warning("Please enter a research question first.")

st.markdown(
    """
    <div class="footer-note">
        AI Research Agent · Week 5 of a 90-Day AI Engineering Roadmap · Developed by <b>Hamna Munir</b>
    </div>
    """,
    unsafe_allow_html=True,
)
