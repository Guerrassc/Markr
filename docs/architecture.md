# Architecture (M3, running product)

```mermaid
flowchart LR
  U["Student in browser"] -->|"brief and draft: PDF, TXT or pasted text"| UI["app.py<br/>Streamlit UI"]
  UI -->|"PDF"| PDF["markr/pdf_text.py<br/>pypdf"]
  PDF -->|"text, page count"| UI
  UI -->|"brief text"| EX["markr/extract.py<br/>prompt: extract_requirements_v2"]
  UI -->|"requirements + draft text"| CK["markr/check.py<br/>prompt: check_draft_v1"]
  EX --> LLM["markr/llm.py<br/>HTTP, 3 tries, 45 s timeout"]
  CK --> LLM
  LLM -->|"JSON request"| G[["Google Gemini API<br/>gemini-3.5-flash-lite"]]
  G -->|"JSON answer"| LLM
  LLM --> V["markr/validate.py<br/>quote must appear in the text"]
  V -->|"checked checklist or verdicts"| UI
  ENV[".env: GEMINI_API_KEY, MARKR_MODEL_SMALL"] -.-> LLM
  subgraph OUT["Trust boundary: text leaves your computer"]
    G
  end
```

- **Model:** `gemini-3.5-flash-lite` through the Gemini `generateContent` endpoint, temperature 0, JSON output. The name is read from `.env`.
- **Data stores:** none. The checklist and results live in the Streamlit session (memory) and disappear when the page is reloaded.
- **Trust boundary:** the brief text and, for the check, the draft text are sent to Google. Nothing else leaves the machine. The API key stays in the local `.env`, which is not committed.
- **Code checks around the AI:** a requirement is dropped when its `source_quote` is not found in the brief; a "met" becomes "uncertain" when its evidence is not found in the draft; word and page counts are computed by code.
- **Failure handling:** retries on 429/5xx/timeouts, then a message on screen.