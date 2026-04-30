import tempfile
import unittest
from pathlib import Path

from voice_agent_demo.cli import build_pipeline


class VoiceAgentPipelineTest(unittest.TestCase):
    def test_pipeline_generates_response_artifact(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            transcript = tmp_path / "input.txt"
            output = tmp_path / "response.txt"
            transcript.write_text("There is mold on my apartment wall.", encoding="utf-8")

            result = build_pipeline().run_turn(transcript, output)

            self.assertEqual(result["turn_count"], 1)
            self.assertIn("mold", result["user_text"].lower())
            self.assertTrue(output.exists())
            self.assertIn("maintenance", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

