"""Tiny provider-agnostic chat client (anthropic | openai | gemini | ollama) using plain HTTP."""
import os, time

def chat(provider, model, system, user, timeout=120):
    import requests
    t0 = time.time()
    if provider == "anthropic":
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": model, "max_tokens": 1500, "system": system,
                  "messages": [{"role": "user", "content": user}]}, timeout=timeout)
        r.raise_for_status(); d = r.json()
        return ("".join(b.get("text", "") for b in d["content"]),
                d["usage"]["input_tokens"], d["usage"]["output_tokens"], time.time() - t0)
    if provider == "openai":
        r = requests.post(os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions",
            headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
            json={"model": model, "messages": [{"role": "system", "content": system},
                                               {"role": "user", "content": user}]}, timeout=timeout)
        r.raise_for_status(); d = r.json()
        return (d["choices"][0]["message"]["content"],
                d["usage"]["prompt_tokens"], d["usage"]["completion_tokens"], time.time() - t0)
    if provider == "gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        hdr = {"x-goog-api-key": os.environ["GEMINI_API_KEY"], "content-type": "application/json"}
        body = {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "generationConfig": {"maxOutputTokens": 4000}}
        for attempt in range(6):
            t0 = time.time()
            r = requests.post(url, headers=hdr, json=body, timeout=timeout)
            if r.status_code in (429, 503) and attempt < 5:
                time.sleep(min(60, 5 * 2 ** attempt))
                continue
            break
        time.sleep(8)
        r.raise_for_status(); d = r.json()
        text = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
        u = d.get("usageMetadata", {})
        return (text, u.get("promptTokenCount", 0), u.get("candidatesTokenCount", 0), time.time() - t0)
    if provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        r = requests.post(host + "/api/chat",
            json={"model": model, "stream": False, "messages": [{"role": "system", "content": system},
                                                                {"role": "user", "content": user}]}, timeout=timeout)
        r.raise_for_status(); d = r.json()
        return (d["message"]["content"], d.get("prompt_eval_count", 0), d.get("eval_count", 0), time.time() - t0)
    raise ValueError("MARKR_PROVIDER must be anthropic, openai, gemini or ollama")
