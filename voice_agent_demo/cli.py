import argparse
import json

from voice_agent_demo.pipeline import VoiceAgentPipeline
from voice_agent_demo.providers import RuleBasedAssistant, TextFileTTS, TranscriptFileSTT


def build_pipeline():
    return VoiceAgentPipeline(
        stt_provider=TranscriptFileSTT(),
        assistant_provider=RuleBasedAssistant(),
        tts_provider=TextFileTTS(),
    )


def main():
    parser = argparse.ArgumentParser(description="Run the local voice-agent pipeline demo.")
    parser.add_argument("--transcript", required=True, help="Path to input transcript text")
    parser.add_argument("--output", default="out/response.txt", help="Path for response artifact")
    args = parser.parse_args()

    result = build_pipeline().run_turn(args.transcript, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

