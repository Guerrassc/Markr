# Architecture sketch (M2, first version)

```mermaid
flowchart LR
  U[Student] -->|uploads brief and draft| UI[Web UI]
  UI --> API[Markr backend]
  API -->|reads| P[(prompts/extract_requirements.txt)]
  API -->|brief text and draft text| LLM[[LLM API: Google Gemini API, model to be chosen]]
  LLM -->|checklist as JSON| API
  API --> UI
  ENV[.env with API key, git-ignored] -.-> API
  subgraph OUT[Data that leaves our system]
    LLM
  end
```

- Prompts live in `prompts/`; model names and the API key come from `.env` (never committed).
- Brief and draft text are sent to the API provider; nothing is stored by Markr in this first version.
- This is the M2 sketch. The final package needs a diagram exported as PNG or SVG that names every external API and model with its version.
