"""M2 experiment: how well can we pull the requirements out of an assignment brief?

Three approaches, same 10 briefs (cases.json):
  rules - dumb baseline, regex for dates / numbers with units / "no, not, must" clauses
  small - cheaper LLM (MARKR_MODEL_SMALL)
  large - stronger LLM (MARKR_MODEL_LARGE)

Score = recall: a labelled requirement counts as found if one extracted line contains all its key words.
Run: python experiments/m2_extraction/run_experiment.py [--approaches rules,small,large]
"""
import argparse, json, os, re, statistics, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december|janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre"
UNITS = "words?|pages?|minutes?|slides?|sources?|references?|problems?|questions?|charts?|members?|%|cm|pt"

def load_env():
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def norm(t):
    t = t.lower().replace("-", " ").replace("\u2013", " ")
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)
    return re.sub(r"\s+", " ", t)

def rules_extract(brief):
    out = []
    out += [m.group(0) for m in re.finditer(rf"\d{{1,2}} (?:{MONTHS})(?: \d{{4}})?", brief, re.I)]
    out += [m.group(0) for m in re.finditer(rf"(?:at least |max(?:imum)? |about )?\d+(?:[.,]\d+)?[ -]?(?:{UNITS})\b[^.;,]*", brief, re.I)]
    out += [m.group(0) for m in re.finditer(r"\b(?:no|not|must|do not|don't|only)\b[^.;]*", brief, re.I)]
    return out

def llm_extract(provider, model, brief):
    from llm import chat
    system = (ROOT / "prompts" / "extract_requirements.txt").read_text(encoding="utf-8")
    text, tin, tout, secs = chat(provider, model, system, brief)
    a, b = text.find("["), text.rfind("]")
    try:
        items = [str(x) for x in json.loads(text[a:b + 1])]
    except Exception:
        items = [l.strip("-* \t") for l in text.splitlines() if l.strip()]
    return items, tin, tout, secs

def recall(items, gt):
    lines = [norm(i) for i in items]
    found = [any(all(norm(k) in line for k in keys) for line in lines) for keys in gt]
    return sum(found) / len(gt), [g for g, f in zip(gt, found) if not f]

def main():
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--approaches", default="rules,small,large")
    names = ap.parse_args().approaches.split(",")
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    provider = os.environ.get("MARKR_PROVIDER", "")
    summary, detail = {}, {}
    for name in names:
        model = os.environ.get(f"MARKR_MODEL_{name.upper()}", "") if name != "rules" else "regex"
        if name != "rules" and not (provider and model):
            print(f"[skip] {name}: set MARKR_PROVIDER and MARKR_MODEL_{name.upper()} in .env"); continue
        recs, counts, tin, tout, lats, rows = [], [], 0, 0, [], []
        for c in cases:
            try:
                if name == "rules":
                    items, a, b, s = rules_extract(c["brief"]), 0, 0, 0.0
                else:
                    items, a, b, s = llm_extract(provider, model, c["brief"])
            except Exception as e:
                print(f"[error] {name}/{c['id']}: {e}"); continue
            r, missed = recall(items, c["gt"])
            recs.append(r); counts.append(len(items)); tin += a; tout += b; lats.append(s)
            rows.append({"case": c["id"], "recall": round(r, 2), "n_items": len(items), "missed": missed, "items": items})
        if not recs:
            continue
        summary[name] = {"model": model, "cases": len(recs), "mean_recall": round(statistics.mean(recs), 3),
                         "mean_items": round(statistics.mean(counts), 1), "input_tokens": tin, "output_tokens": tout,
                         "median_latency_s": round(statistics.median(lats), 2), "worst_latency_s": round(max(lats), 2)}
        detail[name] = rows
    out = ROOT / "results"; out.mkdir(exist_ok=True)
    (out / "m2_results.json").write_text(json.dumps({"summary": summary, "detail": detail}, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["| approach | model | cases | mean recall | items/brief | in tok | out tok | median s | worst s |", "|---|---|---|---|---|---|---|---|---|"]
    for n, s in summary.items():
        md.append(f"| {n} | {s['model']} | {s['cases']} | {s['mean_recall']:.0%} | {s['mean_items']} | {s['input_tokens']} | {s['output_tokens']} | {s['median_latency_s']} | {s['worst_latency_s']} |")
    (out / "m2_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))

if __name__ == "__main__":
    main()
