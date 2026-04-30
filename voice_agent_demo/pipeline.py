from dataclasses import dataclass, field


@dataclass
class ConversationTurn:
    user: str
    assistant: str


@dataclass
class VoiceAgentPipeline:
    stt_provider: object
    assistant_provider: object
    tts_provider: object
    history: list[ConversationTurn] = field(default_factory=list)

    def run_turn(self, input_path, output_path):
        user_text = self.stt_provider.transcribe(input_path)
        response_text = self.assistant_provider.respond(user_text, history=self.history)
        artifact_path = self.tts_provider.synthesize(response_text, output_path)
        self.history.append(ConversationTurn(user=user_text, assistant=response_text))

        return {
            "user_text": user_text,
            "response_text": response_text,
            "artifact_path": str(artifact_path),
            "turn_count": len(self.history),
        }

