# Voice AI Agent Demo

A local voice-agent framework demo that shows how speech input, conversational reasoning, response synthesis, tracing, and batch evaluation can be wired as separate components.

This repo is intentionally provider-light: the default demo runs without API keys or audio hardware, while the architecture mirrors the STT -> LLM -> TTS flow used in production voice AI systems.

## What It Demonstrates

- Voice-agent pipeline design
- Separate STT, assistant, and TTS provider boundaries
- Conversation memory across turns
- Tool-style routing for common support intents
- Streaming-style response artifact generation
- Per-stage latency traces for STT, assistant, and TTS
- Silence timeout handling
- Low-confidence transcript clarification
- Simulated barge-in / interruption handling
- Batch scenario evaluation with intent accuracy reports
- p50/p95 latency summaries, event counts, and safety-note counts
- Testable code instead of a one-off notebook
- Safe local defaults with no committed secrets
- GitHub Actions CI workflow for tests, sample runs, and batch report generation

## Architecture

```text
transcript/audio input
  -> SpeechToText provider
  -> turn normalization
  -> assistant / tool routing
  -> TextToSpeech provider
  -> response artifact
```

The default providers are mock/local providers:

- `TranscriptFileSTT`: reads a text transcript and optional confidence/event directives
- `RuleBasedAssistant`: handles common support-style intents, silence, low-confidence transcripts, and interruptions with deterministic logic
- `TextFileTTS`: writes the assistant response to a text artifact to stand in for synthesized audio
- `ChunkedTextTTS`: simulates streaming TTS by writing response chunks line by line

These interfaces can be replaced with real providers such as Whisper/faster-whisper for STT, Groq/OpenAI/local LLMs for reasoning, and ElevenLabs/XTTS/pyttsx3 for TTS.

## Quick Start

Run one transcript:

```bash
python -m voice_agent_demo.cli run --transcript examples/sample_transcript.txt --output out/response.txt
```

Run a streaming-style artifact:

```bash
python -m voice_agent_demo.cli run --transcript examples/rent_notice.txt --output out/rent_response.txt --streaming
```

Run the batch scenario suite and create reports:

```bash
python -m voice_agent_demo.cli batch --scenarios examples/scenarios.jsonl --output-dir reports
```

Run a simulated interruption:

```bash
python -m voice_agent_demo.cli run --transcript examples/barge_in_gas.txt --output out/barge_in_response.txt
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Transcript Directives

The local STT provider supports simple comment directives at the top of a transcript file:

```text
# confidence: 0.42
# event: barge_in
Stop, I smell gas now and need help.
```

Supported behavior:

- `# confidence: 0.42` triggers clarification when confidence is below the assistant threshold.
- `# event: silence` simulates no useful speech and avoids committing the turn to conversation history.
- `# event: barge_in` simulates the user interrupting playback and routes the new transcript as the active turn.

## Example

Input transcript:

```text
My apartment wall has mold near the window. What should I do first?
```

Output:

```text
It sounds like a property maintenance issue...
```

Structured result:

```json
{
  "intent": "property_maintenance",
  "confidence": 0.91,
  "transcript_confidence": 1.0,
  "events": [],
  "traces": [
    { "stage": "stt", "latency_ms": 0.0 },
    { "stage": "assistant", "latency_ms": 0.0 },
    { "stage": "tts", "latency_ms": 0.0 }
  ]
}
```

## Project Structure

```text
.
|-- examples/
|   |-- barge_in_gas.txt
|   |-- emergency_gas.txt
|   |-- low_confidence_wall.txt
|   |-- rent_notice.txt
|   |-- sample_transcript.txt
|   |-- silence.txt
|   `-- scenarios.jsonl
|-- reports/
|   |-- batch_report.json
|   |-- batch_report.md
|   `-- *_response.txt
|-- tests/
|   `-- test_pipeline.py
|-- voice_agent_demo/
|   |-- cli.py
|   |-- evaluation.py
|   |-- models.py
|   |-- pipeline.py
|   |-- providers.py
|   `-- tracing.py
|-- pyproject.toml
|-- README.md
`-- requirements.txt
```

## Why This Matters

Voice AI work is easy to describe vaguely and hard to inspect. This demo makes the pipeline boundaries, scenario behavior, and latency traces visible without requiring paid APIs or live audio hardware.

## Repository Quality

- [ROADMAP.md](ROADMAP.md) explains how the demo can mature toward a production-style voice AI prototype.
- [CONTRIBUTING.md](CONTRIBUTING.md) documents local setup and contribution expectations.
- [SECURITY.md](SECURITY.md) documents data-handling rules for transcripts, recordings, and credentials.
- `.github/workflows/ci.yml` runs tests and sample CLI checks on GitHub Actions.

Voice AI systems fail when the audio pipeline, language model, and response layer are tangled together. This demo keeps them separate so latency, replacement providers, testing, and safety checks can be handled independently.

## Next Extensions

- Add `faster-whisper` STT adapter
- Add real streaming TTS adapter
- Add websocket or LiveKit transport
- Add evaluation tests for conversation quality
- Add tool adapters for CRM, calendar, ticketing, or property-management systems
