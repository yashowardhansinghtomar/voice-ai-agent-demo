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
    latency_summary = {}
    event_counts = {}
    safety_note_counts = {}

    for stage in ("stt", "assistant", "tts"):
        values = [
            trace["latency_ms"]
            for result in results
            for trace in result["result"]["traces"]
            if trace["stage"] == stage
        ]
        average_latency[stage] = round(sum(values) / len(values), 3) if values else 0
        latency_summary[stage] = summarize_latency(values)

    for result in results:
        turn = result["result"]
        for event in turn.get("events", []):
            event_counts[event] = event_counts.get(event, 0) + 1
        for note in turn.get("safety_notes", []):
            safety_note_counts[note] = safety_note_counts.get(note, 0) + 1

    return {
        "scenario_count": total,
        "intent_accuracy": round(matches / total, 3) if total else 0,
        "average_latency_ms": average_latency,
        "latency_summary_ms": latency_summary,
        "event_counts": event_counts,
        "safety_note_counts": safety_note_counts,
        "results": results,
    }


def percentile(values, percentile_value):
    if not values:
        return 0
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return round(sorted_values[0], 3)
    index = (len(sorted_values) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = index - lower
    return round(sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight, 3)


def summarize_latency(values):
    if not values:
        return {"avg": 0, "p50": 0, "p95": 0, "max": 0}
    return {
        "avg": round(sum(values) / len(values), 3),
        "p50": percentile(values, 0.5),
        "p95": percentile(values, 0.95),
        "max": round(max(values), 3),
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
        "| Stage | Avg ms | P50 ms | P95 ms | Max ms |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for stage, values in summary.get("latency_summary_ms", {}).items():
        lines.append(
            f"| {stage} | {values['avg']} | {values['p50']} | {values['p95']} | {values['max']} |"
        )

    if summary.get("event_counts"):
        lines.extend(["", "## Event Counts", "", "| Event | Count |", "| --- | ---: |"])
        for event, count in sorted(summary["event_counts"].items()):
            lines.append(f"| {event} | {count} |")

    if summary.get("safety_note_counts"):
        lines.extend(["", "## Safety Note Counts", "", "| Note | Count |", "| --- | ---: |"])
        for note, count in sorted(summary["safety_note_counts"].items()):
            lines.append(f"| {note} | {count} |")

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
                f"- Transcript confidence: {turn.get('transcript_confidence', 1.0)}",
                f"- Events: {', '.join(turn.get('events', [])) if turn.get('events') else 'none'}",
                f"- Intent match: {result['intent_match']}",
                f"- Response artifact: `{turn['artifact_path']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_json(summary, output_path):
    Path(output_path).write_text(json.dumps(summary, indent=2), encoding="utf-8")
