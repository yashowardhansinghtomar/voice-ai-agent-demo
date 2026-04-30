from pathlib import Path

from voice_agent_demo.models import AssistantResponse, TranscriptResult


class TranscriptFileSTT:
    """Reads a transcript file using the same boundary a real STT provider would use."""

    provider_name = "transcript-file"

    def transcribe(self, input_path):
        raw_text = Path(input_path).read_text(encoding="utf-8")
        metadata, body_lines = self._parse_directives(raw_text.splitlines())
        text = "\n".join(body_lines).strip()
        events = self._parse_events(metadata.get("event", ""))
        confidence = self._parse_confidence(metadata.get("confidence", "1.0"))
        return TranscriptResult(
            text=text,
            confidence=confidence,
            events=events,
            metadata=metadata,
        )

    def _parse_directives(self, lines):
        metadata = {}
        body_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") and ":" in stripped:
                key, value = stripped[1:].split(":", 1)
                metadata[key.strip().lower()] = value.strip()
                continue
            body_lines.append(line)

        return metadata, body_lines

    def _parse_confidence(self, value):
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 1.0
        return min(max(confidence, 0.0), 1.0)

    def _parse_events(self, value):
        return [
            event.strip().lower().replace("-", "_")
            for event in value.split(",")
            if event.strip()
        ]


class RuleBasedAssistant:
    """Deterministic assistant used for local demos, tests, and intent routing examples."""

    provider_name = "rule-based-assistant"

    def __init__(self, min_transcript_confidence=0.65):
        self.min_transcript_confidence = min_transcript_confidence

    def respond(self, user_text, history=None, transcript=None):
        text = user_text.lower()
        history = history or []
        transcript = transcript or TranscriptResult(text=user_text)

        if transcript.is_silence:
            return AssistantResponse(
                text=(
                    "I did not catch that. Could you repeat the issue in one short sentence?"
                ),
                intent="silence_timeout",
                confidence=0.98,
                safety_notes=["silence_detected"],
                commit_to_history=False,
            )

        if transcript.confidence < self.min_transcript_confidence:
            return AssistantResponse(
                text=(
                    "I may have misheard that. Could you confirm the issue before I suggest next steps?"
                ),
                intent="clarification_request",
                confidence=transcript.confidence,
                safety_notes=["low_confidence_transcript"],
                commit_to_history=False,
            )

        barge_in = "barge_in" in transcript.events

        if any(term in text for term in ("emergency", "fire", "gas", "electrical shock")):
            return self._with_barge_in(
                AssistantResponse(
                    text=(
                        "This sounds urgent. Move to a safe place first, contact emergency services "
                        "or the relevant utility provider, and avoid handling the issue yourself."
                    ),
                    intent="emergency_escalation",
                    confidence=0.94,
                    safety_notes=["emergency_escalation"],
                ),
                barge_in=barge_in,
            )

        if any(term in text for term in ("mold", "leak", "crack", "wall", "window")):
            return self._with_barge_in(
                AssistantResponse(
                    text=(
                        "It sounds like a property maintenance issue. Document it with photos, "
                        "check for active leaks, improve ventilation if safe, and notify the landlord "
                        "or property manager in writing with a clear repair request."
                    ),
                    intent="property_maintenance",
                    confidence=0.91,
                ),
                barge_in=barge_in,
            )

        if any(term in text for term in ("rent", "deposit", "landlord", "notice", "lease")):
            return self._with_barge_in(
                AssistantResponse(
                    text=(
                        "This may involve tenancy rules. Keep written records, check your lease, "
                        "and verify the notice requirements in your local jurisdiction before taking action."
                    ),
                    intent="tenancy_guidance",
                    confidence=0.87,
                    safety_notes=["jurisdiction_specific_advice"],
                ),
                barge_in=barge_in,
            )

        if history:
            return self._with_barge_in(
                AssistantResponse(
                    text="I can help continue from the previous turn. Could you share the specific issue or goal?",
                    intent="follow_up",
                    confidence=0.62,
                ),
                barge_in=barge_in,
            )

        return self._with_barge_in(
            AssistantResponse(
                text="I can help with property issues, tenancy questions, and next-step planning. What happened?",
                intent="general_help",
                confidence=0.55,
            ),
            barge_in=barge_in,
        )

    def _with_barge_in(self, response, barge_in=False):
        if not barge_in:
            return response
        response.text = f"I stopped the previous response. {response.text}"
        if "barge_in_handled" not in response.safety_notes:
            response.safety_notes.append("barge_in_handled")
        return response


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
