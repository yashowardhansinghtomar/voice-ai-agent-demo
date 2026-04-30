from dataclasses import dataclass, field
from pathlib import Path

from voice_agent_demo.models import ConversationTurn, TurnResult
from voice_agent_demo.tracing import stage_timer


@dataclass
class VoiceAgentPipeline:
    stt_provider: object
    assistant_provider: object
    tts_provider: object
    history: list[ConversationTurn] = field(default_factory=list)

    def run_turn(self, input_path, output_path):
        traces = []

        with stage_timer("stt", traces, provider=self.stt_provider.provider_name):
            user_text = self.stt_provider.transcribe(input_path)

        with stage_timer("assistant", traces, provider=self.assistant_provider.provider_name):
            assistant_response = self.assistant_provider.respond(user_text, history=self.history)

        with stage_timer("tts", traces, provider=self.tts_provider.provider_name):
            artifact_path = self.tts_provider.synthesize(assistant_response.text, output_path)

        self.history.append(
            ConversationTurn(
                user=user_text,
                assistant=assistant_response.text,
                intent=assistant_response.intent,
                confidence=assistant_response.confidence,
            )
        )

        return TurnResult(
            user_text=user_text,
            response_text=assistant_response.text,
            intent=assistant_response.intent,
            confidence=assistant_response.confidence,
            artifact_path=str(artifact_path),
            turn_count=len(self.history),
            traces=traces,
            safety_notes=assistant_response.safety_notes,
        )

    def run_batch(self, scenarios, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        for index, scenario in enumerate(scenarios, start=1):
            transcript_path = Path(scenario["transcript_path"])
            output_path = output_dir / f"{scenario['id']}_response.txt"
            result = self.run_turn(transcript_path, output_path)
            results.append(
                {
                    "id": scenario["id"],
                    "expected_intent": scenario.get("expected_intent"),
                    "result": result.to_dict(),
                    "intent_match": result.intent == scenario.get("expected_intent"),
                }
            )

        return results

