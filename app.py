"""
🧠 Research Mind — Multi-Agent Research System UI
A polished Streamlit dashboard for `run_research_pipeline` from pipeline.py.

Run locally:
    pip install streamlit
    streamlit run app.py
"""

import time
import io
import sys
import threading
import streamlit as st

# ---- Import your pipeline pieces directly so we can drive each agent and
# show live "running / done" status instead of one big black-box call. ----
from agents import build_search_agent, build_read_agent, writer_chain, critic_chain


# ============================================================
# PAGE CONFIG + GLOBAL STYLES
# ============================================================
st.set_page_config(
    page_title="Research Mind • Multi-Agent System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* App background gradient */
    .stApp {
        background: radial-gradient(1200px 600px at 10% -10%, #1e293b 0%, transparent 60%),
                    radial-gradient(1000px 500px at 100% 0%, #312e81 0%, transparent 55%),
                    linear-gradient(180deg, #0b1220 0%, #0a0f1c 100%);
        color: #e5e7eb;
    }

    /* Hero */
    .hero {
        padding: 28px 32px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(236,72,153,0.12));
        border: 1px solid rgba(148,163,184,0.18);
        backdrop-filter: blur(8px);
        margin-bottom: 18px;
    }
    .hero h1 {
        font-size: 2.2rem;
        margin: 0;
        background: linear-gradient(90deg, #a5b4fc, #f0abfc, #fda4af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .hero p { color: #cbd5e1; margin-top: 6px; }

    /* Agent card */
    .agent-card {
        display: flex; align-items: center; gap: 14px;
        padding: 14px 16px;
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(15,23,42,0.55);
        margin-bottom: 10px;
        transition: all .25s ease;
    }
    .agent-card.running {
        border-color: rgba(96,165,250,0.65);
        box-shadow: 0 0 0 3px rgba(59,130,246,0.18), 0 8px 30px -10px rgba(59,130,246,0.45);
        background: rgba(30,58,138,0.35);
    }
    .agent-card.done {
        border-color: rgba(34,197,94,0.55);
        background: rgba(6,78,59,0.25);
    }
    .agent-card.pending { opacity: 0.65; }

    .agent-icon {
        width: 44px; height: 44px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(148,163,184,0.18);
    }
    .agent-meta { flex: 1; }
    .agent-title { font-weight: 700; color: #f1f5f9; font-size: 0.98rem; }
    .agent-sub { color: #94a3b8; font-size: 0.82rem; margin-top: 2px; }

    .status-pill {
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em;
        padding: 5px 10px; border-radius: 999px; text-transform: uppercase;
    }
    .pill-pending { background: rgba(148,163,184,0.18); color: #cbd5e1; }
    .pill-running { background: rgba(59,130,246,0.22); color: #93c5fd; }
    .pill-done    { background: rgba(34,197,94,0.20);  color: #86efac; }
    .pill-error   { background: rgba(239,68,68,0.22);  color: #fca5a5; }

    /* Spinning dot for running */
    .spinner {
        width: 10px; height: 10px; border-radius: 50%;
        background: #60a5fa;
        box-shadow: 0 0 0 0 rgba(96,165,250,0.7);
        animation: pulse 1.2s infinite;
        display: inline-block; margin-right: 6px;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(96,165,250,0.7); }
        70%  { box-shadow: 0 0 0 10px rgba(96,165,250,0); }
        100% { box-shadow: 0 0 0 0 rgba(96,165,250,0); }
    }

    /* Stat tiles */
    .stat {
        padding: 14px 16px; border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(15,23,42,0.55);
    }
    .stat .label { color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; }
    .stat .value { color: #f8fafc; font-size: 1.4rem; font-weight: 800; margin-top: 4px; }

    /* Report panel */
    .report {
        padding: 22px 26px; border-radius: 16px;
        background: rgba(15,23,42,0.65);
        border: 1px solid rgba(148,163,184,0.18);
    }

    /* Hide default Streamlit chrome a bit */
    #MainMenu, footer { visibility: hidden; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================
st.markdown(
    """
    <div class="hero">
        <h1>🧠 Research Mind</h1>
        <p>A multi-agent research system — Search → Read → Write → Critique. Live agent telemetry below.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — INPUT
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Research Settings")
    topic = st.text_area(
        "Research topic",
        placeholder="e.g. Impact of generative AI on scientific peer review (2024–2025)",
        height=110,
    )
    st.caption("Tip: be specific — include scope, timeframe, and angle.")
    run_btn = st.button("🚀 Run Research Pipeline", type="primary", use_container_width=True)
    st.divider()
    st.markdown("#### 🤖 Agents")
    st.markdown(
        "- 🔎 **Search Agent** — finds sources\n"
        "- 📖 **Reader Agent** — scrapes & extracts\n"
        "- ✍️ **Writer Agent** — drafts the report\n"
        "- 🧪 **Critic Agent** — reviews & scores"
    )


# ============================================================
# AGENT DEFINITIONS
# ============================================================
AGENTS = [
    {"key": "search",  "icon": "🔎", "title": "Search Agent",  "sub": "Finding recent, reliable sources"},
    {"key": "read",    "icon": "📖", "title": "Reader Agent",  "sub": "Scraping & extracting content"},
    {"key": "writer",  "icon": "✍️", "title": "Writer Agent",  "sub": "Drafting structured report"},
    {"key": "critic",  "icon": "🧪", "title": "Critic Agent",  "sub": "Reviewing & scoring quality"},
]


def render_agent_panel(placeholder, statuses, timings):
    """Render the live agent status panel."""
    html = ['<div>']
    for a in AGENTS:
        s = statuses.get(a["key"], "pending")
        t = timings.get(a["key"])
        time_str = f" • {t:.1f}s" if t is not None else ""

        if s == "running":
            pill = '<span class="status-pill pill-running"><span class="spinner"></span>Running</span>'
            cls = "running"
        elif s == "done":
            pill = '<span class="status-pill pill-done">✓ Done</span>'
            cls = "done"
        elif s == "error":
            pill = '<span class="status-pill pill-error">✕ Error</span>'
            cls = "done"
        else:
            pill = '<span class="status-pill pill-pending">Pending</span>'
            cls = "pending"

        html.append(
f"""<div class="agent-card {cls}">
    <div class="agent-icon">{a['icon']}</div>
    <div class="agent-meta">
        <div class="agent-title">{a['title']}</div>
        <div class="agent-sub">{a['sub']}{time_str}</div>
    </div>
    {pill}
</div>"""
        )
    html.append("</div>")
    placeholder.markdown("".join(html), unsafe_allow_html=True)


def extract_content(result):
    """Pull text content from LangChain message-like or plain results."""
    if isinstance(result, dict) and "messages" in result:
        last = result["messages"][-1]
        return getattr(last, "content", str(last))
    return getattr(result, "content", str(result))


# ============================================================
# RUN PIPELINE
# ============================================================
if "results" not in st.session_state:
    st.session_state.results = None

if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    # Layout: agent panel on the left, live progress on the right
    left, right = st.columns([1, 1.2], gap="large")
    with left:
        st.markdown("#### 🛰️ Agent Pipeline")
        agent_panel = st.empty()
    with right:
        st.markdown("#### 📡 Live Progress")
        progress = st.progress(0, text="Initializing pipeline…")
        status_box = st.empty()

    statuses = {a["key"]: "pending" for a in AGENTS}
    timings = {}
    render_agent_panel(agent_panel, statuses, timings)

    results = {}
    overall_start = time.time()

    try:
        # ---- 1) SEARCH AGENT ----
        statuses["search"] = "running"
        render_agent_panel(agent_panel, statuses, timings)
        status_box.info("🔎 Searching the web for high-signal sources…")
        progress.progress(10, text="Search Agent working…")
        t0 = time.time()

        search_agent = build_search_agent()
        search_results = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        results["search"] = extract_content(search_results)

        timings["search"] = time.time() - t0
        statuses["search"] = "done"
        render_agent_panel(agent_panel, statuses, timings)
        progress.progress(35, text="Search complete ✓")

        # ---- 2) READER AGENT ----
        statuses["read"] = "running"
        render_agent_panel(agent_panel, statuses, timings)
        status_box.info("📖 Reading and extracting content from sources…")
        t0 = time.time()

        read_agent = build_read_agent()
        read_results = read_agent.invoke({
            "messages": [("user", f"Read and extract key information from these sources:\n{results['search']}")]
        })
        results["read"] = extract_content(read_results)

        timings["read"] = time.time() - t0
        statuses["read"] = "done"
        render_agent_panel(agent_panel, statuses, timings)
        progress.progress(60, text="Reading complete ✓")

        # ---- 3) WRITER AGENT ----
        statuses["writer"] = "running"
        render_agent_panel(agent_panel, statuses, timings)
        status_box.info("✍️ Writing structured research report…")
        t0 = time.time()

        draft = writer_chain.invoke({"topic": topic, "research": results["read"]})
        results["draft"] = extract_content(draft)

        timings["writer"] = time.time() - t0
        statuses["writer"] = "done"
        render_agent_panel(agent_panel, statuses, timings)
        progress.progress(85, text="Draft complete ✓")

        # ---- 4) CRITIC AGENT ----
        statuses["critic"] = "running"
        render_agent_panel(agent_panel, statuses, timings)
        status_box.info("🧪 Critiquing and scoring the draft…")
        t0 = time.time()

        critique = critic_chain.invoke({"report": results["draft"]})
        results["critic"] = extract_content(critique)

        timings["critic"] = time.time() - t0
        statuses["critic"] = "done"
        render_agent_panel(agent_panel, statuses, timings)
        progress.progress(100, text="All agents finished ✓")
        status_box.success(f"✅ Research complete in {time.time() - overall_start:.1f}s")

        results["topic"] = topic
        results["total_time"] = time.time() - overall_start
        results["timings"] = timings
        st.session_state.results = results

    except Exception as e:
        # mark current running agent as error
        for k, v in statuses.items():
            if v == "running":
                statuses[k] = "error"
        render_agent_panel(agent_panel, statuses, timings)
        status_box.error(f"❌ Pipeline failed: {e}")
        st.exception(e)
        st.stop()


# ============================================================
# RESULTS
# ============================================================
res = st.session_state.results
if res:
    st.markdown("---")

    # Stat tiles
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat"><div class="label">Total Time</div><div class="value">{res["total_time"]:.1f}s</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat"><div class="label">Search</div><div class="value">{res["timings"].get("search",0):.1f}s</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat"><div class="label">Reader</div><div class="value">{res["timings"].get("read",0):.1f}s</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat"><div class="label">Writer</div><div class="value">{res["timings"].get("writer",0):.1f}s</div></div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"### 📌 Topic\n> {res['topic']}")

    tab1, tab2, tab3, tab4 = st.tabs(["📄 Final Report", "🧪 Critic Feedback", "🔎 Sources", "📖 Scraped Content"])

    with tab1:
        st.markdown('<div class="report">', unsafe_allow_html=True)
        st.markdown(res.get("draft", "_No draft produced._"))
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download Report (Markdown)",
            data=res.get("draft", ""),
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab2:
        st.markdown('<div class="report">', unsafe_allow_html=True)
        st.markdown(res.get("critic", "_No critique produced._"))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        with st.expander("Show raw search results", expanded=True):
            st.markdown(res.get("search", "_No search output._"))

    with tab4:
        with st.expander("Show scraped content", expanded=True):
            st.markdown(res.get("read", "_No scraped content._"))
else:
    st.info("👈 Enter a topic in the sidebar and click **Run Research Pipeline** to begin.")
