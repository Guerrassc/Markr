import requests
import streamlit as st

from markr.check import check_draft
from markr.extract import extract_requirements
from markr.llm import LLMUnavailable
from markr.pdf_text import read_pdf
from markr.theme import build_css, requirement_row, section, stats_html
from markr.validate import word_count

st.set_page_config(page_title="Markr", layout="centered")

if "dark" not in st.session_state:
    st.session_state["dark"] = False


def flip_theme():
    st.session_state["dark"] = not st.session_state["dark"]


with st.container(key="theme_toggle"):
    st.button("Light mode" if st.session_state["dark"] else "Dark mode",
              key="theme_btn", on_click=flip_theme)

st.markdown(build_css(st.session_state["dark"]), unsafe_allow_html=True)


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


st.markdown(
    '<div class="mk-brand">Markr</div>'
    '<div class="mk-tagline">Turn an assignment brief into a checklist, then check your draft against it.</div>'
    '<div class="mk-note">Your brief and draft are sent to Google Gemini for analysis. '
    "Only upload text you are allowed to share. Markr checks your work, it never writes it.</div>",
    unsafe_allow_html=True,
)

st.markdown(section("01", "Assignment brief"), unsafe_allow_html=True)
brief_file = st.file_uploader("Brief (PDF or TXT)", type=["pdf", "txt"], key="brief_file")
brief_paste = st.text_area("Or paste the brief text", height=150)

if st.button("Extract requirements", type="primary"):
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
    st.markdown(f'<div class="mk-sub">Checklist, {len(requirements)} requirements</div>', unsafe_allow_html=True)
    dropped = st.session_state.get("dropped")
    if dropped:
        st.markdown(
            f'<div class="mk-small">{dropped} proposed requirement(s) were removed because their quote was not found in the brief.</div>',
            unsafe_allow_html=True,
        )
    rows = "".join(requirement_row(r) for r in requirements)
    st.markdown(f'<div class="mk-list">{rows}</div>', unsafe_allow_html=True)

    st.markdown(section("02", "Your draft"), unsafe_allow_html=True)
    draft_file = st.file_uploader("Draft (PDF or TXT)", type=["pdf", "txt"], key="draft_file")
    draft_paste = st.text_area("Or paste your draft", height=150)

    if st.button("Check my draft", type="primary"):
        draft_text, pages = get_text(draft_file, draft_paste)
        if not draft_text.strip():
            st.error("No text found in the draft. Scanned PDFs are not supported, paste the text instead.")
        else:
            results = run_ai(check_draft, requirements, draft_text, pages)
            if results is not None:
                st.session_state["results"] = results
                st.session_state["counts"] = (word_count(draft_text), pages)

if st.session_state.get("results"):
    results = st.session_state["results"]
    words, pages = st.session_state["counts"]
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("met", "missing", "uncertain")}
    st.markdown(section("03", "Results"), unsafe_allow_html=True)
    st.markdown(stats_html(words, pages, counts), unsafe_allow_html=True)
    rows = "".join(
        requirement_row(r, status=r["status"], evidence=r["evidence"], note=r["note"]) for r in results
    )
    st.markdown(f'<div class="mk-list">{rows}</div>', unsafe_allow_html=True)