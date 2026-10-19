"""Fill the red [...] results cells of the M2 page from results/m2_results.json.

Usage (from the repo root, after running the experiment):
    python tools/fill_m2.py --template docs/M2_unilu.tex --out docs/M2_filled.tex

Every number comes from your results file; nothing is made up. If an approach did not run
(or some requests failed) the text says so. Prices are the Gemini list prices checked on
19 Oct 2026 (paid tier, per 1M tokens); update PRICES if you use other models.
"""
import argparse, json, sys
from pathlib import Path

PRICES = {  # model -> (input, output) USD per 1M tokens
    "gemini-3.8-flash": (0.75, 3.75),
    "gemini-3.5-flash-lite": (0.30, 2.50),
}

def esc(t):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"), ("$", r"\$")]:
        t = t.replace(a, b)
    return t

def sub(s, old, new):
    if old not in s:
        print("[warn] placeholder not found:", old[:60]); return s
    return s.replace(old, new, 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="docs/M2_unilu.tex")
    ap.add_argument("--out", default="docs/M2_filled.tex")
    ap.add_argument("--results", default="results/m2_results.json")
    ap.add_argument("--cases", default="experiments/m2_extraction/cases.json")
    a = ap.parse_args()

    res = json.loads(Path(a.results).read_text(encoding="utf-8"))
    summ, detail = res["summary"], res["detail"]
    gt_len = {c["id"]: len(c["gt"]) for c in json.loads(Path(a.cases).read_text(encoding="utf-8"))}
    s = Path(a.template).read_text(encoding="utf-8")

    def per_approach(name):
        if name not in summ:
            return {"recall": "not run", "lat": "not run", "fail": "not run"}
        m = summ[name]
        rows = detail[name]
        total = sum(gt_len[r["case"]] for r in rows)
        missed = [(r["case"], k) for r in rows for k in r["missed"]]
        ex = "; ".join(f"{c}: {' + '.join(k)}" for c, k in missed[:1]) or "none"
        return {"recall": rf"{m['mean_recall']*100:.0f}\,\%",
                "lat": f"{m['median_latency_s']} s / {m['worst_latency_s']} s",
                "fail": esc(f"missed {len(missed)} of {total} (e.g. {ex})")}

    small, large = per_approach("small"), per_approach("large")
    for key in ("recall", "lat", "fail"):
        old = {"recall": r"\todo{from results}", "lat": r"\todo{s / s}", "fail": r"\todo{from failed cases}"}[key]
        s = sub(s, old, small[key])
        s = sub(s, old, large[key])

    base = summ.get("rules", {}).get("mean_recall", 0.5)
    ran = [n for n in ("small", "large") if n in summ]
    if not ran:
        sys.exit("No LLM results found in " + a.results)
    best = max(ran, key=lambda n: summ[n]["mean_recall"])
    lines = []
    for n in ran:
        m = summ[n]
        lines.append(esc(f"{n} ({m['model']}) {m['mean_recall']*100:.0f}% recall at {m['mean_items']} items per brief, "
                         f"median {m['median_latency_s']} s"))
    table = "; ".join(lines)
    com = [f"The best LLM ({esc(summ[best]['model'])}) found {summ[best]['mean_recall']*100:.0f}\\,\\% of the labelled requirements against {base*100:.0f}\\,\\% for the regex baseline."]
    misses = [(r["case"], k) for r in detail[best] for k in r["missed"]][:2]
    if misses:
        com.append("It still missed " + esc("; ".join(f"{c}: {' + '.join(k)}" for c, k in misses)) + ".")
    if len(ran) == 2:
        d = (summ["large"]["mean_recall"] - summ["small"]["mean_recall"]) * 100
        com.append(f"The large model scored {d:+.0f} points compared with the small one.")
    for n in ran:
        if summ[n]["cases"] < 10:
            com.append(f"Only {summ[n]['cases']} of 10 requests completed for {n} (likely rate limits); the others are excluded.")
    com.append("With only 10 synthetic briefs these numbers are rough.")
    s = sub(s, r"LLM rows: \todo{paste table}. \textbf{Commentary:} \todo{what the LLMs found that rules missed; two or three concrete missed items; any failures}.",
            f"LLM rows: {table}. \\textbf{{Commentary:}} {' '.join(com)}")

    # chosen model: small if within 5 points of large, otherwise the best one
    if len(ran) == 2 and summ["small"]["mean_recall"] >= summ["large"]["mean_recall"] - 0.05:
        pick, why = "small", "it is within 5 points of the large model and costs less per action"
    else:
        pick, why = best, "it found the most requirements in the experiment"
    s = sub(s, r"\todo{gemini-3.8-flash or gemini-3.5-flash-lite}", esc(summ[pick]["model"]))
    s = sub(s, r"\todo{reason from the results}", why)
    s = sub(s, r"\todo{model}", esc(summ[pick]["model"]))

    m = summ[pick]
    n = max(m["cases"], 1)
    tin, tout = m["input_tokens"] / n, m["output_tokens"] / n
    cost = ""
    if m["model"] in PRICES:
        pi, po = PRICES[m["model"]]
        cost = f", about \\${(tin*pi + tout*po)/1e6:.5f} per brief at the prices above"
    meas = esc(f"In the experiment, extraction alone averaged {tin:.0f} input and {tout:.0f} output tokens per brief ({m['model']})") + cost + "."
    s = sub(s, r"\todo{replace with measured tokens from \texttt{results/m2\_results.json}}", meas)

    Path(a.out).write_text(s, encoding="utf-8")
    left = s.count(r"\todo{")
    print(f"Wrote {a.out}. Red [..] items still to fill by hand: {left}")

if __name__ == "__main__":
    main()
