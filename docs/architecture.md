# Architecture sketch (M2)

```mermaid
flowchart LR
  U[Student] -->|brief PDF/text and draft| UI[Markr UI]
  UI --> API[Markr backend]
  API -->|read prompt| P[prompts/extract_requirements.txt]
  API -->|brief text| LLM[[Google Gemini API\ngemini-3.5-flash-lite]]
  LLM -->|checklist| API
  API -->|checklist + draft| CMP[Draft comparison]
  CMP -->|met / missing / uncertain| UI
  ENV[Local .env API key] -.-> API
  subgraph OUT[Data leaves Markr]
    LLM
  end
```

- The model and API key are configured in the local `.env`; only `.env.example` is committed. The key must never be committed.
- The extraction prompt is versioned in `prompts/`.
- Assignment brief text (and, for the draft-checking feature, draft text) is sent to Google Gemini. The student reviews and can edit the extracted checklist before relying on it.
- This is the proposed M2 architecture, not a claim that the complete UI/product already exists. The M3 diagram must be updated to match the running implementation and identify every API/model version, data store and trust boundary.
