from pathlib import Path

from voice_agent_demo.models import AssistantResponse


class TranscriptFileSTT:
    """Reads a transcript file using the same boundary a real STT provider would use."""

    provider_name = "transcript-file"

    def transcribe(self, input_path):
        return Path(input_path).read_text(encoding="utf-8").strip()


class RuleBasedAssistant:
    """Deterministic assistant used for local demos, tests, and intent routing examples."""

    provider_name = "rule-based-assistant"

    def respond(self, user_text, history=None):
        text = user_text.lower()
        history = history or []

        if any(term in text for term in ("mold", "leak", "crack", "wall", "window")):
            return AssistantResponse(
                text=(
                    "It sounds like a property maintenance issue. Document it with photos, "
                    "check for active leaks, improve ventilation if safe, and notify the landlord "
                    "or property manager in writing with a clear repair request."
                ),
                intent="property_maintenance",
                confidence=0.91,
            )

        if any(term in text for term in ("rent", "deposit", "landlord", "notice", "lease")):
            return AssistantResponse(
                text=(
                    "This may involve tenancy rules. Keep written records, check your lease, "
                    "and verify the notice requirements in your local jurisdiction before taking action."
                ),
                intent="tenancy_guidance",
                confidence=0.87,
                safety_notes=["jurisdiction_specific_advice"],
            )

        if any(term in text for term in ("emergency", "fire", "gas", "electrical shock")):
            return AssistantResponse(
                text=(
                    "This sounds urgent. Move to a safe place first, contact emergency services "
                    "or the relevant utility provider, and avoid handling the issue yourself."
                ),
                intent="emergency_escalation",
                confidence=0.94,
                safety_notes=["emergency_escalation"],
            )

        if history:
            return AssistantResponse(
                text="I can help continue from the previous turn. Could you share the specific issue or goal?",
                intent="follow_up",
                confidence=0.62,
            )

        return AssistantResponse(
            text="I can help with property issues, tenancy questions, and next-step planning. What happened?",
            intent="general_help",
            confidence=0.55,
        )


class TextFileTTS:
    """Writes the assistant response as a text artifact in place of synthesized audio."""

    provider_name = "text-file-tts"

    def synthesize(self, text, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        return output_path


class ChunkedTextTTS(TextFileTTS):
    """Simulates streaming by writing response chunks line by line."""

    provider_name = "chunked-text-tts"

    def __init__(self, chunk_size=80):
        self.chunk_size = chunk_size

    def synthesize(self, text, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        chunks = [
            text[index : index + self.chunk_size]
            for index in range(0, len(text), self.chunk_size)
        ]
        output_path.write_text("\n".join(chunks), encoding="utf-8")
        return output_path

