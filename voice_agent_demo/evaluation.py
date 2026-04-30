import json
from pathlib import Path


def load_scenarios(path):
    scenarios = []
    base_dir = Path(path).resolve().parent
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            scenario = json.loads(line)
            if "id" not in scenario or "transcript_path" not in scenario:
                raise ValueError(f"Scenario line {line_number} must include id and transcript_path")
            transcript_path = Path(scenario["transcript_path"])
            if not transcript_path.is_absolute():
                scenario["transcript_path"] = str((base_dir / transcript_path).resolve())
            scenarios.append(scenario)
    return scenarios


def summarize_batch(results):
    total = len(results)
    matches = sum(1 for result in results if result["intent_match"])
    average_latency = {}

    for stage in ("stt", "assistant", "tts"):
        values = [
            trace["latency_ms"]
            for result in results
            for trace in result["result"]["traces"]
            if trace["stage"] == stage
        ]
        average_latency[stage] = round(sum(values) / len(values), 3) if values else 0

    return {
        "scenario_count": total,
        "intent_accuracy": round(matches / total, 3) if total else 0,
        "average_latency_ms": average_latency,
        "results": results,
    }


def render_markdown(summary):
    lines = [
        "# Voice Agent Batch Report",
        "",
        f"Scenarios: `{summary['scenario_count']}`",
        f"Intent accuracy: `{summary['intent_accuracy']}`",
        "",
        "## Average Latency",
        "",
        "| Stage | Latency ms |",
        "| --- | ---: |",
    ]
    for stage, latency in summary["average_latency_ms"].items():
        lines.append(f"| {stage} | {latency} |")

    lines.extend(["", "## Scenario Results", ""])
    for result in summary["results"]:
        turn = result["result"]
        lines.extend(
            [
                f"### {result['id']}",
                "",
                f"- Expected intent: {result['expected_intent']}",
                f"- Predicted intent: {turn['intent']}",
                f"- Confidence: {turn['confidence']}",
                f"- Intent match: {result['intent_match']}",
                f"- Response artifact: `{turn['artifact_path']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_json(summary, output_path):
    Path(output_path).write_text(json.dumps(summary, indent=2), encoding="utf-8")

