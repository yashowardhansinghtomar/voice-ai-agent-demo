import json
import tempfile
import unittest
from pathlib import Path

from voice_agent_demo.cli import build_pipeline, main
from voice_agent_demo.evaluation import load_scenarios, render_markdown, summarize_batch


class VoiceAgentPipelineTest(unittest.TestCase):
    def test_pipeline_generates_traced_response_artifact(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            transcript = tmp_path / "input.txt"
            output = tmp_path / "response.txt"
            transcript.write_text("There is mold on my apartment wall.", encoding="utf-8")

            result = build_pipeline().run_turn(transcript, output)

            self.assertEqual(result.turn_count, 1)
            self.assertEqual(result.intent, "property_maintenance")
            self.assertGreaterEqual(result.confidence, 0.9)
            self.assertIn("mold", result.user_text.lower())
            self.assertTrue(output.exists())
            self.assertIn("maintenance", output.read_text(encoding="utf-8"))
            self.assertEqual(["stt", "assistant", "tts"], [trace.stage for trace in result.traces])
            self.assertTrue(all(trace.latency_ms >= 0 for trace in result.traces))

    def test_streaming_tts_writes_chunked_artifact(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            transcript = tmp_path / "input.txt"
            output = tmp_path / "response.txt"
            transcript.write_text("My landlord sent a notice about rent.", encoding="utf-8")

            result = build_pipeline(streaming=True).run_turn(transcript, output)

            self.assertEqual(result.intent, "tenancy_guidance")
            self.assertEqual(result.safety_notes, ["jurisdiction_specific_advice"])
            self.assertIn("\n", output.read_text(encoding="utf-8"))

    def test_batch_scenarios_create_accuracy_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            first = tmp_path / "mold.txt"
            second = tmp_path / "gas.txt"
            scenario_path = tmp_path / "scenarios.jsonl"
            output_dir = tmp_path / "reports"
            first.write_text("Mold is growing by the window.", encoding="utf-8")
            second.write_text("I smell gas and feel unsafe.", encoding="utf-8")
            scenario_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "id": "maintenance",
                                "transcript_path": "mold.txt",
                                "expected_intent": "property_maintenance",
                            }
                        ),
                        json.dumps(
                            {
                                "id": "emergency",
                                "transcript_path": "gas.txt",
                                "expected_intent": "emergency_escalation",
                            }
                        ),
                    ]
                ),
                encoding="utf-8",
            )

            scenarios = load_scenarios(scenario_path)
            results = build_pipeline().run_batch(scenarios, output_dir)
            summary = summarize_batch(results)
            report = render_markdown(summary)

            self.assertEqual(summary["scenario_count"], 2)
            self.assertEqual(summary["intent_accuracy"], 1.0)
            self.assertIn("Average Latency", report)
            self.assertTrue((output_dir / "maintenance_response.txt").exists())

    def test_cli_batch_writes_reports(self):
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "batch"

            exit_code = main(
                [
                    "batch",
                    "--scenarios",
                    str(project_root / "examples" / "scenarios.jsonl"),
                    "--output-dir",
                    str(output_dir),
                    "--streaming",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "batch_report.md").exists())
            self.assertTrue((output_dir / "batch_report.json").exists())


if __name__ == "__main__":
    unittest.main()
