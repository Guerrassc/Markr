import requests
import streamlit as st

from markr.check import check_draft
from markr.extract import extract_requirements
from markr.llm import LLMUnavailable
from markr.pdf_text import read_pdf
from markr.validate import word_count

LABELS = {"met": "✅ Met", "missing": "❌ Missing", "uncertain": "❓ Uncertain"}


def get_text(uploaded, pasted):
    if uploaded is None:
        return pasted, None
    if uploaded.name.lower().endswith(".pdf"):
        return read_pdf(uploaded)
    return uploaded.read().decode("utf-8", errors="ignore"), None


def run_ai(fn, *args):
    try:
        with st.spinner("Asking the AI, this can take up to a minute..."):
            return fn(*args)
    except LLMUnavailable as e:
        st.error(f"The AI service did not answer ({e}). Please try again in a minute.")
    except requests.HTTPError:
        st.error("The AI service refused the request. Check the API key in your .env file.")
    except KeyError:
        st.error("A setting is missing in .env (GEMINI_API_KEY or MARKR_MODEL_SMALL).")
    except ValueError:
        st.error("The AI answer could not be read. Please try again.")
    return None


st.set_page_config(page_title="Markr")
st.title("Markr")
st.caption("Makes a checklist from an assignment brief and checks your draft against it. It never writes your work.")
st.warning("Your brief and draft are sent to Google Gemini. Only upload text you are allowed to share.")

st.header("1. Assignment brief")
brief_file = st.file_uploader("Brief (PDF or TXT)", type=["pdf", "txt"], key="brief_file")
brief_paste = st.text_area("Or paste the brief text", height=150)

if st.button("Extract requirements"):
    brief_text, _ = get_text(brief_file, brief_paste)
    if not brief_text.strip():
        st.error("No text found. Scanned PDFs are not supported, paste the text instead.")
    else:
        out = run_ai(extract_requirements, brief_text)
        if out is not None:
            kept, rejected = out
            st.session_state.pop("results", None)
            st.session_state["requirements"] = kept
            st.session_state["dropped"] = len(rejected)
            if not kept:
                st.error("No verified requirements were found. Try again or paste clearer text.")

requirements = st.session_state.get("requirements")
if requirements:
    st.subheader("Checklist")
    if st.session_state.get("dropped"):
        st.caption(f"{st.session_state['dropped']} requirement(s) were dropped because their quote is not in the brief.")
    for r in requirements:
        st.markdown(f"- **{r['requirement']}**")
        st.caption(f"From the brief: “{r['source_quote']}”")

    st.header("2. Your draft")
    draft_file = st.file_uploader("Draft (PDF or TXT)", type=["pdf", "txt"], key="draft_file")
    draft_paste = st.text_area("Or paste your draft", height=150)

    if st.button("Check my draft"):
        draft_text, pages = get_text(draft_file, draft_paste)
        if not draft_text.strip():
            st.error("No text found in the draft. Scanned PDFs are not supported, paste the text instead.")
        else:
            results = run_ai(check_draft, requirements, draft_text, pages)
            if results is not None:
                st.session_state["results"] = results
                st.session_state["counts"] = (word_count(draft_text), pages)

if st.session_state.get("results"):
    words, pages = st.session_state["counts"]
    st.header("Result")
    st.info(f"Words: {words}" + (f" | Pages: {pages}" if pages else ""))
    for r in st.session_state["results"]:
        st.markdown(f"**{LABELS[r['status']]}** - {r['requirement']}")
        st.caption(f"Brief: “{r['source_quote']}”")
        if r["evidence"]:
            st.caption(f"Evidence in your draft: “{r['evidence']}”")
        if r["note"]:
            st.caption(r["note"])