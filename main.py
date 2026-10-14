"""
Liquid d1 Multimodal Support Triage Engine (Zero-Token System 1)
Evaluates customer complaints and attached damage photos using the Ollama-registered liquid-d1 model.
"""

import base64
import json
import os
from pathlib import Path
import time
import requests

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "liquid-d1")

QUESTIONS_SCHEMA = {
    "visual_damage": {"type": "noul", "instructions": "Does the photo show physical breakage or damage?"},
    "team": {
        "type": "choice",
        "instructions": "Which department handles this claim?",
        "criteria": {
            "fragile_replacements": "Damaged ceramic tableware, plates, glassware, bowls, or shattered mugs",
            "hazardous_appliance": "Cracked induction cooktops, glass stoves, or electrical fire hazards",
            "baggage_logistics": "Damaged luggage, cracked hard-shell suitcases, or airport baggage claims",
        },
    },
    "severity": {
        "type": "score",
        "instructions": "How severe is the item damage?",
        "criteria": ["Minor aesthetic scratch", "Moderate single break", "Severe breakage or hazard"],
    },
}


def query_liquid_d1(image_path: str, message: str) -> dict:
    """Queries the Ollama-registered liquid-d1 model with multimodal image + text payload."""
    start = time.perf_counter()
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        f"State: {message}\n"
        f"Questions: {json.dumps(QUESTIONS_SCHEMA)}\n"
        "Output: calibrated decision distribution (zero token System 1)"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "format": "json",
    }

    resp = requests.post(OLLAMA_API_URL, json=payload)
    resp.raise_for_status()

    raw_response = resp.json().get("response", "{}")
    ans = json.loads(raw_response) if isinstance(raw_response, str) else raw_response

    return {
        "raw_response": ans,
        "damage_prob": ans.get("visual_damage", {}).get("noul"),
        "team": ans.get("team", {}).get("choice"),
        "team_conf": ans.get("team", {}).get("confidence"),
        "severity_score": ans.get("severity", {}).get("score"),
        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
    }


def generate_reply(team: str) -> str:
    """Forms customer reply based on routed department."""
    actions = {
        "hazardous_appliance": "Please unplug the unit immediately. Our team has expedited a full replacement and refund.",
        "baggage_logistics": "We have opened a priority baggage claim and issued a courier inspection credit to your account.",
        "fragile_replacements": "Your breakage claim is approved. A reinforced replacement has been scheduled for delivery.",
    }
    return actions.get(team, "Your inquiry has been verified and forwarded to our specialist team.")


def export_report(evaluations: list, output_file: Path):
    """Outputs compact decision markdown table."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Liquid d1 Multimodal Support Triage Report",
        "",
        f"- Target Model: **{MODEL_NAME} (Ollama)** | Modality: Vision + Text | Output Tokens: **0 tokens**",
        f"- Average Latency: {sum(e['results']['latency_ms'] for e in evaluations) / len(evaluations):.2f} ms",
        "",
        "| Case | Image | Assigned Team | Severity | Damage P(yes) | Latency | Automated Reply |",
        "|---|---|---|---|---|---|---|",
    ]
    for ev in evaluations:
        c, r = ev["case"], ev["results"]
        team_display = str(r["team"]).replace('_', ' ').title() if r["team"] else "Pending"
        conf_display = f" ({r['team_conf']*100:.0f}%)" if r["team_conf"] is not None else ""
        sev_display = f"{r['severity_score']}/3.0" if r["severity_score"] is not None else "N/A"
        prob_display = f"{r['damage_prob']}" if r["damage_prob"] is not None else "N/A"

        lines.append(
            f"| Case {c['id']} | `{c['image']}` | **{team_display}**{conf_display} "
            f"| {sev_display} | {prob_display} | {r['latency_ms']} ms | *\"{r['reply']}\"* |"
        )

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    print("=" * 60)
    print(f"Liquid d1 Multimodal Triage via Ollama [{MODEL_NAME}]")
    print("=" * 60)

    with open(Path("inputs") / "complaints.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    evaluations = []
    for c in cases:
        res = query_liquid_d1(str(Path("inputs") / c["image"]), c["message"])
        res["reply"] = generate_reply(res["team"])
        evaluations.append({"case": c, "results": res})
        print(f"Case {c['id']}: {res['team']} | Latency: {res['latency_ms']} ms")

    out_file = Path("outputs") / "outputs.md"
    export_report(evaluations, out_file)
    print(f"\nTriage complete. Report saved to {out_file}")


if __name__ == "__main__":
    main()
