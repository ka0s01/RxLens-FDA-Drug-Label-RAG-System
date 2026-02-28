import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="RxLens", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:         #06090f;
    --surface:    #0d1117;
    --surface-2:  #161b27;
    --border:     #1f2d3d;
    --border-2:   #263545;
    --accent:     #2563eb;
    --accent-glow:#1d4ed8;
    --teal:       #0d9488;
    --text-1:     #f0f4f8;
    --text-2:     #8ba0b8;
    --text-3:     #3d5470;
    --success:    #10b981;
    --warning:    #f59e0b;
    --danger:     #ef4444;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: var(--bg) !important; color: var(--text-1) !important; }

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── header ── */
.rxlens-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.rxlens-wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.04em;
    color: var(--text-1);
    line-height: 1;
}
.rxlens-wordmark span { color: var(--accent); }
.rxlens-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.18em;
    margin-top: 0.45rem;
}
.status-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.dot { width:7px; height:7px; border-radius:50%; background:var(--success); }
.dot.off { background: var(--danger); }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
    margin-bottom: 2rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-3) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 0.9rem 1.5rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text-1) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── inputs ── */
.stTextInput label, .stSelectbox label, .stFileUploader label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: var(--text-3) !important;
    margin-bottom: 0.4rem !important;
}
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: var(--text-3) !important; }

div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-1) !important;
}
[data-baseweb="popover"] { background: var(--surface-2) !important; border: 1px solid var(--border) !important; }
[role="option"] { background: var(--surface-2) !important; color: var(--text-2) !important; }
[role="option"]:hover { background: var(--border) !important; color: var(--text-1) !important; }

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border-2) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] * { color: var(--text-2) !important; }
[data-testid="stFileUploader"] section { background: transparent !important; }

/* ── buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1.6rem !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover  { background: var(--accent-glow) !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* ── answer card ── */
.answer-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1.75rem 2rem;
    margin: 1.25rem 0 2rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    color: var(--text-1);
}

/* ── source chips ── */
.src-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-3);
    margin-bottom: 0.6rem;
}
.src-chip {
    display: inline-block;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.28rem 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-2);
    margin: 0.2rem 0.2rem 0.2rem 0;
    letter-spacing: 0.02em;
}

/* ── drug library ── */
.drug-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.15s;
}
.drug-row:hover { border-color: var(--border-2); }
.drug-row-name {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: var(--text-1);
    letter-spacing: -0.01em;
}
.drug-row-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.6rem;
    border-radius: 100px;
    background: rgba(16,185,129,0.1);
    color: var(--success);
    border: 1px solid rgba(16,185,129,0.25);
}

/* ── stat cards ── */
.stats-row { display:flex; gap:0.75rem; margin-bottom:2rem; }
.stat-card {
    flex:1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem 1.4rem;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.9rem;
    color: var(--text-1);
    line-height: 1;
}
.stat-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.13em;
    margin-top: 0.35rem;
}

/* ── upload instructions ── */
.instr {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
}
.instr-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-3);
    margin-bottom: 0.8rem;
}
.instr p {
    font-family: 'Inter', sans-serif;
    font-size: 0.83rem;
    color: var(--text-2);
    line-height: 1.9;
    margin: 0;
}
.instr strong { color: var(--text-1); font-weight: 500; }

/* ── alerts ── */
.stAlert {
    background: var(--surface) !important;
    border-radius: 7px !important;
    border: 1px solid var(--border) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
div[data-testid="stNotificationContentSuccess"] { border-left: 3px solid var(--success) !important; }
div[data-testid="stNotificationContentWarning"] { border-left: 3px solid var(--warning) !important; }
div[data-testid="stNotificationContentError"]   { border-left: 3px solid var(--danger)  !important; }

/* ── spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── search bar on library page ── */
.stTextInput.search input { border-radius: 100px !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 3px; }

/* ── misc ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }
.stMarkdown p { color: var(--text-2); font-family: 'Inter', sans-serif; font-size: 0.875rem; }
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

# ── Header ──────────────────────────────────────────────────────────────────
dot_class = "dot" if api_online else "dot off"
api_label  = f"{len(drugs)} labels indexed" if api_online else "API offline"

st.markdown(f"""
<div class="rxlens-header">
    <div>
        <div class="rxlens-wordmark">Rx<span>Lens</span></div>
        <div class="rxlens-sub">FDA Drug Label Intelligence</div>
    </div>
    <div class="status-pill">
        <span class="{dot_class}"></span>
        {api_label}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_query, tab_library, tab_upload = st.tabs(["Ask a Question", "Drug Library", "Upload Label"])


# ── TAB 1: Query ──────────────────────────────────────────────────────────────
with tab_query:
    col_q, col_f = st.columns([3, 1])

    with col_q:
        question = st.text_input(
            "Question",
            placeholder="e.g. Can I take warfarin with aspirin?",
            key="question_input"
        )
    with col_f:
        options = ["All drugs"] + drugs
        selected = st.selectbox("Filter by drug", options, key="drug_select")

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
                    data = res.json()
                    answer  = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])

                    st.markdown('<div class="src-label">Answer</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="answer-wrap">{answer}</div>', unsafe_allow_html=True)

                    if sources:
                        unique_sources = list(dict.fromkeys(sources))
                        st.markdown('<div class="src-label">Sources</div>', unsafe_allow_html=True)
                        chips = "".join(f'<span class="src-chip">{s}</span>' for s in unique_sources)
                        st.markdown(chips, unsafe_allow_html=True)

                except requests.exceptions.Timeout:
                    st.error("Request timed out. The model may still be loading — try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ── TAB 2: Drug Library ───────────────────────────────────────────────────────
with tab_library:
    if not api_online:
        st.error("API is offline. Start the FastAPI server and refresh.")
    else:
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-val">{len(drugs)}</div>
                <div class="stat-lbl">Indexed Labels</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">8</div>
                <div class="stat-lbl">Sections per Label</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">FDA</div>
                <div class="stat-lbl">Data Source</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if drugs:
            search = st.text_input("Search", placeholder="Filter drugs...", key="lib_search", label_visibility="collapsed")
            filtered = [d for d in drugs if search.lower() in d.lower()] if search else drugs
            st.markdown("<br>", unsafe_allow_html=True)

            for drug in filtered:
                st.markdown(f"""
                <div class="drug-row">
                    <div>
                        <div class="drug-row-name">{drug}</div>
                        <div class="drug-row-meta">FDA Prescribing Information</div>
                    </div>
                    <span class="badge">Indexed</span>
                </div>
                """, unsafe_allow_html=True)

            if not filtered:
                st.markdown('<p style="color:var(--text-3);text-align:center;padding:2rem 0;">No matching drugs.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:var(--text-3);">No labels indexed yet. Upload one to get started.</p>', unsafe_allow_html=True)


# ── TAB 3: Upload ─────────────────────────────────────────────────────────────
with tab_upload:
    if not api_online:
        st.error("API is offline. Start the FastAPI server and refresh.")
    else:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            drug_name = st.text_input("Drug name", placeholder="e.g. Metformin", key="upload_drug_name")
        with col_b:
            uploaded_file = st.file_uploader("PDF Label", type=["pdf"], key="pdf_uploader")

        if st.button("Ingest Label", key="ingest_btn"):
            if not drug_name.strip():
                st.warning("Enter a drug name before uploading.")
            elif not uploaded_file:
                st.warning("Select a PDF file before ingesting.")
            else:
                with st.spinner(f"Processing {drug_name}..."):
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
                            st.warning(f"{drug_name} is already indexed — no changes made.")
                        else:
                            st.success(f"{drug_name} ingested successfully — {data.get('chunks', 0)} chunks indexed.")
                            fetch_drugs.clear()
                            st.rerun()

                    except requests.exceptions.Timeout:
                        st.error("Processing timed out. Large PDFs can take a while — check the API terminal.")
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")

        st.markdown("""
        <div class="instr">
            <div class="instr-title">How to get FDA labels</div>
            <p>
                Go to <strong>dailymed.nlm.nih.gov</strong> and search for the drug by generic name.<br>
                Select the prescription label — not the OTC consumer label.<br>
                Download the PDF and upload it here. Use the exact generic name as the drug name.
            </p>
        </div>
        """, unsafe_allow_html=True)