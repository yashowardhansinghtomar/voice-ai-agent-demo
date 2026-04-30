import argparse
import json
import sys
from pathlib import Path

from voice_agent_demo.evaluation import (
    load_scenarios,
    render_markdown,
    summarize_batch,
    write_json,
)
from voice_agent_demo.pipeline import VoiceAgentPipeline
from voice_agent_demo.providers import (
    ChunkedTextTTS,
    RuleBasedAssistant,
    TextFileTTS,
    TranscriptFileSTT,
)


def build_pipeline(streaming=False):
    return VoiceAgentPipeline(
        stt_provider=TranscriptFileSTT(),
        assistant_provider=RuleBasedAssistant(),
        tts_provider=ChunkedTextTTS() if streaming else TextFileTTS(),
    )


def command_run(args):
    result = build_pipeline(streaming=args.streaming).run_turn(args.transcript, args.output)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def command_batch(args):
    scenarios = load_scenarios(args.scenarios)
    pipeline = build_pipeline(streaming=args.streaming)
    results = pipeline.run_batch(scenarios, args.output_dir)
    summary = summarize_batch(results)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / "batch_report.md"
    json_path = output_dir / "batch_report.json"
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")
    write_json(summary, json_path)

    print(json.dumps({"markdown": str(markdown_path), "json": str(json_path)}, indent=2))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Run the local voice-agent pipeline demo.")
    subparsers = parser.add_subparsers(dest="command")

    run = subparsers.add_parser("run", help="Run one transcript through the voice pipeline")
    run.add_argument("--transcript", required=True, help="Path to input transcript text")
    run.add_argument("--output", default="out/response.txt", help="Path for response artifact")
    run.add_argument("--streaming", action="store_true", help="Use chunked text output")
    run.set_defaults(func=command_run)

    batch = subparsers.add_parser("batch", help="Run multiple transcript scenarios")
    batch.add_argument("--scenarios", required=True, help="Path to scenarios JSONL")
    batch.add_argument("--output-dir", default="out/batch", help="Directory for reports and artifacts")
    batch.add_argument("--streaming", action="store_true", help="Use chunked text output")
    batch.set_defaults(func=command_batch)

    return parser


def main(argv=None):
    parser = build_parser()
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv and argv[0].startswith("--"):
        argv = ["run", *argv]

    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
