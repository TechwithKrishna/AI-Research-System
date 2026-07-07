import streamlit as st
from datetime import datetime

from pipelines import run_research_pipeline

st.set_page_config(page_title="AI Research System", page_icon="🔍", layout="wide")

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔍 AI Research System")
    st.markdown("Multi-agent pipeline: **Search → Read → Write → Critique**")
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        """
        1. **Search Agent** finds recent, reliable sources
        2. **Reader Agent** scrapes the most relevant page
        3. **Writer Chain** drafts a full report
        4. **Critic Chain** reviews and gives feedback
        """
    )
    st.divider()
    if st.session_state.history:
        st.markdown("### Recent Topics")
        for h in reversed(st.session_state.history[-5:]):
            if st.button(h, key=f"hist_{h}", use_container_width=True):
                st.session_state.rerun_topic = h

# ---------- Main ----------
st.title("AI Multi-Agent Research Assistant")
st.markdown(
    "Enter a topic below and the agent pipeline will research, write, "
    "and critique a full report for you."
)

with st.form("research_form"):
    default_topic = st.session_state.pop("rerun_topic", "")
    topic = st.text_input(
        "Research topic",
        value=default_topic,
        placeholder="e.g. Latest advances in quantum computing",
    )
    submitted = st.form_submit_button("Run Research", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic to research.")
    else:
        with st.spinner("Running the pipeline — search, read, write, critique... this can take a minute or two."):
            try:
                result = run_research_pipeline(topic)
                st.session_state.result = result
                st.session_state.history.append(topic)
                st.success("Pipeline complete!")
            except Exception as e:
                st.session_state.result = None
                st.error(f"Something went wrong while running the pipeline: {e}")

# ---------- Results ----------
if st.session_state.result:
    result = st.session_state.result
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Final Report", "🧐 Feedback", "🔎 Search Results", "📖 Scraped Content"]
    )

    with tab1:
        st.subheader("Final Report")
        report = result.get("Report", "")
        st.markdown(str(report) if report else "_No report generated._")
        if report:
            st.download_button(
                "Download Report (.md)",
                data=str(report),
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    with tab2:
        st.subheader("Critic Feedback")
        feedback = result.get("Feedback", "")
        st.markdown(str(feedback) if feedback else "_No feedback generated._")

    with tab3:
        st.subheader("Raw Search Results")
        st.text_area(
            "Search Results",
            value=str(result.get("search_result", "")),
            height=400,
            label_visibility="collapsed",
        )

    with tab4:
        st.subheader("Scraped Content")
        st.text_area(
            "Scraped Content",
            value=str(result.get("scraped_content", "")),
            height=400,
            label_visibility="collapsed",
        )
else:
    st.info("Run a research topic above to see results here.")