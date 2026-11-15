import os, time, random, requests
from pathlib import Path


class LLMUnavailable(Exception):
    pass


RETRY_STATUS = {429, 500, 502, 503, 504}


def load_env():
    f = Path(__file__).parent.parent / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


load_env()


def ask_gemini(system, user, timeout=45, attempts=3):
    model = os.environ["MARKR_MODEL_SMALL"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"x-goog-api-key": os.environ["GEMINI_API_KEY"],
               "content-type": "application/json"}
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": 4000,
                             "responseMimeType": "application/json"},
    }
    last_error = "unknown error"
    for attempt in range(1, attempts + 1):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=timeout)
            if r.status_code in RETRY_STATUS:
                last_error = f"HTTP {r.status_code}"
            else:
                r.raise_for_status()
                parts = (r.json().get("candidates") or [{}])[0].get("content", {}).get("parts", [])
                text = "".join(p.get("text", "") for p in parts)
                if text:
                    return text
                last_error = "empty response"
        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = type(e).__name__
        if attempt < attempts:
            time.sleep(2 ** attempt + random.uniform(0, 1))
    raise LLMUnavailable(f"No answer after {attempts} attempts ({last_error})")