from pathlib import Path


class TranscriptFileSTT:
    """Reads a transcript file using the same boundary a real STT provider would use."""

    def transcribe(self, input_path):
        return Path(input_path).read_text(encoding="utf-8").strip()


class RuleBasedAssistant:
    """Deterministic assistant used for local demos and tests."""

    def respond(self, user_text, history=None):
        text = user_text.lower()
        history = history or []

        if any(term in text for term in ("mold", "leak", "crack", "wall", "window")):
            return (
                "It sounds like a property maintenance issue. Document it with photos, "
                "check for active leaks, improve ventilation if safe, and notify the landlord "
                "or property manager in writing with a clear repair request."
            )

        if any(term in text for term in ("rent", "deposit", "landlord", "notice")):
            return (
                "This may involve tenancy rules. Keep written records, check your lease, "
                "and verify the notice requirements in your local jurisdiction before taking action."
            )

        if history:
            return "I can help continue from the previous turn. Could you share the specific issue or goal?"

        return "I can help with property issues, tenancy questions, and next-step planning. What happened?"


class TextFileTTS:
    """Writes the assistant response as a text artifact in place of synthesized audio."""

    def synthesize(self, text, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        return output_path

