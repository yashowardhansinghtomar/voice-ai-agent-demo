from dataclasses import dataclass, field
from pathlib import Path

from voice_agent_demo.models import ConversationTurn, TranscriptResult, TurnResult
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
            transcript = self._normalize_transcript(self.stt_provider.transcribe(input_path))

        with stage_timer("assistant", traces, provider=self.assistant_provider.provider_name):
            assistant_response = self.assistant_provider.respond(
                transcript.text,
                history=self.history,
                transcript=transcript,
            )

        with stage_timer("tts", traces, provider=self.tts_provider.provider_name):
            artifact_path = self.tts_provider.synthesize(assistant_response.text, output_path)

        if assistant_response.commit_to_history:
            self.history.append(
                ConversationTurn(
                    user=transcript.text,
                    assistant=assistant_response.text,
                    intent=assistant_response.intent,
                    confidence=assistant_response.confidence,
                )
            )

        return TurnResult(
            user_text=transcript.text,
            response_text=assistant_response.text,
            intent=assistant_response.intent,
            confidence=assistant_response.confidence,
            artifact_path=str(artifact_path),
            turn_count=len(self.history),
            traces=traces,
            safety_notes=assistant_response.safety_notes,
            transcript_confidence=transcript.confidence,
            events=transcript.events,
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

    def _normalize_transcript(self, transcript):
        if isinstance(transcript, TranscriptResult):
            return transcript
        return TranscriptResult(text=str(transcript).strip())
