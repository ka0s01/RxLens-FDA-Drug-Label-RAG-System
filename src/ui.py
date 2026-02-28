import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="RxLens", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Swapped to DM Sans for a friendly, readable, consumer-app vibe */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

:root {
    /* Kept your exact dark mode color scheme */
    --bg:          #0E1117;
    --surface:     #1A1F2E;
    --surface-2:   #222840;
    --border:      #374151;
    --border-2:    #4B5563;
    --accent:      #2563EB;
    --accent-dim:  #1D4ED8;
    --text-1:      #F0F4F8;
    --text-2:      #A0AEC0;
    --text-3:      #6B7280;
    --success:     #10B981;
    --warning:     #F59E0B;
    --danger:      #EF4444;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background: var(--bg) !important;
    color: var(--text-1) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
}

[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── header ── */
.rxlens-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.rxlens-wordmark {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    letter-spacing: -0.02em;
    color: var(--text-1);
    line-height: 1;
}
.rxlens-wordmark span { color: var(--accent); }
.rxlens-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: var(--text-2);
    margin-top: 0.5rem;
}
.status-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.55rem 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-2);
}
.dot     { width: 8px; height: 8px; border-radius: 50%; background: var(--success); flex-shrink: 0; }
.dot.off { background: var(--danger); }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 1rem !important;
    padding: 0 !important;
    margin-bottom: 2.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-2) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    padding: 1rem 1rem !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -1px !important;
    transition: color 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover  { color: var(--text-1) !important; }
.stTabs [aria-selected="true"] {
    color: var(--text-1) !important;
    font-weight: 700 !important;
    border-bottom: 3px solid var(--accent) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── form labels ── */
.stTextInput label,
.stSelectbox label,
.stFileUploader > label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text-1) !important;
    margin-bottom: 0.5rem !important;
}

/* ── text input ── */
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-1) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: var(--text-3) !important; font-weight: 400 !important; }

/* ── select ── */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-1) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
}
[data-baseweb="popover"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[role="option"] {
    background: var(--surface-2) !important;
    color: var(--text-2) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
[role="option"]:hover {
    background: var(--border) !important;
    color: var(--text-1) !important;
}

/* ── file uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border-2) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] * { color: var(--text-2) !important; font-family: 'DM Sans', sans-serif !important;}
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 2rem !important;
}

/* ── button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 2rem !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover  { background: var(--accent-dim) !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* ── metrics ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--text-2) !important;
}

/* ── captions ── */
.stCaption, [data-testid="stCaptionContainer"] p, small {
    color: var(--text-2) !important;
    font-size: 0.95rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── answer card ── */
.answer-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0 2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    line-height: 1.7;
    color: var(--text-1);
}

/* ── section label ── */
.sec-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-1);
    margin-bottom: 0.75rem;
}

/* ── source chips ── */
.src-chip {
    display: inline-block;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-1);
    margin: 0.3rem 0.4rem 0.3rem 0;
}

/* ── drug library rows ── */
.drug-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.15s;
}
.drug-row:hover { border-color: var(--border-2); }
.drug-row-name {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--text-1);
}
.drug-row-meta {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--text-2);
    margin-top: 0.3rem;
}
.indexed-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #10B981;
}
.indexed-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10B981;
}

/* ── instructions ── */
.instr-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin-top: 2.5rem;
}
.instr-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-1);
    margin-bottom: 1.25rem;
}
.instr-step {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
    margin-bottom: 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: var(--text-2);
    line-height: 1.6;
}
.instr-num {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--surface-2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-1);
    margin-top: 0.1rem;
}
.instr-step strong { color: var(--text-1); font-weight: 700; }

/* ── alerts ── */
div[data-testid="stNotification"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── scrollbar ── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-3); }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=10)
def fetch_drugs():
    try:
        r = requests.get(f"{API}/drugs", timeout=3)
        return r.json().get("drugs", []), True
    except Exception:
        return [], False


drugs, api_online = fetch_drugs()

# ── Header ────────────────────────────────────────────────────────────────────
dot_cls   = "dot" if api_online else "dot off"
api_label = f"{len(drugs)} labels indexed" if api_online else "API offline"

st.markdown(f"""
<div class="rxlens-header">
    <div>
        <div class="rxlens-wordmark">Rx<span>Lens</span></div>
        <div class="rxlens-sub">Get insights from FDA drug labels</div>
    </div>
    <div class="status-pill">
        <span class="{dot_cls}"></span>
        {api_label}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_query, tab_library, tab_upload = st.tabs(["Ask a Question", "Drug Library", "Upload Label"])


# ── TAB 1 — Query ─────────────────────────────────────────────────────────────
with tab_query:
    col_q, col_f = st.columns([3, 1])
    with col_q:
        question = st.text_input(
            "Question",
            placeholder="e.g. Can I take warfarin with aspirin?",
            key="q_input"
        )
    with col_f:
        selected = st.selectbox("Filter by drug", ["All drugs"] + drugs, key="drug_select")

    search_clicked = st.button("Search", key="search_btn")

    if search_clicked:
        if not question.strip():
            st.warning("Please enter a question.")
        elif not api_online:
            st.error("API is offline. Start the FastAPI server and refresh.")
        else:
            drug_filter = None if selected == "All drugs" else [selected]
            with st.spinner("Searching labels..."):
                try:
                    res = requests.post(
                        f"{API}/query",
                        json={"question": question, "drug_filter": drug_filter},
                        timeout=120
                    )
                    data    = res.json()
                    answer  = data.get("answer", "No answer returned.")
                    sources = list(dict.fromkeys(data.get("sources", [])))

                    st.markdown('<div class="sec-label" style="margin-top:2rem;">Answer</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="answer-card">{answer}</div>', unsafe_allow_html=True)

                    if sources:
                        st.markdown('<div class="sec-label">Sources</div>', unsafe_allow_html=True)
                        chips = "".join(f'<span class="src-chip">{s}</span>' for s in sources)
                        st.markdown(chips, unsafe_allow_html=True)

                except requests.exceptions.Timeout:
                    st.error("Request timed out. The model may be loading — try again in a moment.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ── TAB 2 — Drug Library ──────────────────────────────────────────────────────
with tab_library:
    if not api_online:
        st.error("API is offline. Start the FastAPI server and refresh.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Indexed Labels", len(drugs))
        col2.metric("Sections per Label", 8)
        col3.metric("Data Source", "FDA")

        st.divider()

        if drugs:
            search = st.text_input(
                "Filter drugs",
                placeholder="Search by name...",
                key="lib_search",
                label_visibility="collapsed"
            )
            st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
            filtered = [d for d in drugs if search.lower() in d.lower()] if search else drugs

            for drug in filtered:
                st.markdown(f"""
                <div class="drug-row">
                    <div>
                        <div class="drug-row-name">{drug}</div>
                        <div class="drug-row-meta">FDA Prescribing Information</div>
                    </div>
                    <span class="indexed-badge">Indexed</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            if not filtered:
                st.caption("No drugs match your search.")
        else:
            st.caption("No labels indexed yet. Go to Upload Label to add one.")


# ── TAB 3 — Upload ────────────────────────────────────────────────────────────
with tab_upload:
    if not api_online:
        st.error("API is offline. Start the FastAPI server and refresh.")
    else:
        drug_name     = st.text_input("Drug name", placeholder="e.g. Metformin", key="upload_name")
        uploaded_file = st.file_uploader("PDF Label", type=["pdf"], key="pdf_upload")

        st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
        ingest_clicked = st.button("Ingest Label", key="ingest_btn")
        st.markdown("</div>", unsafe_allow_html=True)

        if ingest_clicked:
            if not drug_name.strip():
                st.warning("Enter a drug name before uploading.")
            elif not uploaded_file:
                st.warning("Select a PDF file before clicking Ingest.")
            else:
                with st.spinner(f"Processing {drug_name.strip()}..."):
                    try:
                        res = requests.post(
                            f"{API}/ingest",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                            data={"drug_name": drug_name.strip()},
                            timeout=300
                        )
                        data = res.json()
                        msg  = data.get("message", "")

                        if "already" in msg.lower():
                            st.warning(f"{drug_name.strip()} is already indexed — no changes made.")
                        else:
                            st.success(f"{drug_name.strip()} ingested — {data.get('chunks', 0)} chunks indexed.")
                            fetch_drugs.clear()
                            st.rerun()

                    except requests.exceptions.Timeout:
                        st.error("Processing timed out. Large PDFs can take a while — check the API terminal.")
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")

        st.markdown("""
        <div class="instr-block">
            <div class="instr-title">How to get FDA labels from DailyMed</div>
            <div class="instr-step">
                <div class="instr-num">1</div>
                <div>Go to <strong>dailymed.nlm.nih.gov</strong> and search for the drug by generic name.</div>
            </div>
            <div class="instr-step">
                <div class="instr-num">2</div>
                <div>Select the <strong>prescription label</strong> — not the OTC consumer label.</div>
            </div>
            <div class="instr-step">
                <div class="instr-num">3</div>
                <div>Download the PDF and upload it above using the exact <strong>generic drug name</strong>.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)