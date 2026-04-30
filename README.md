# Voice AI Agent Demo

A small, testable voice-agent pipeline that shows how speech input, conversational reasoning, and speech output can be wired as separate components.

This repo is intentionally provider-light: the default demo runs without API keys or audio hardware, while the architecture mirrors the STT -> LLM -> TTS flow used in production voice AI systems.

## What It Demonstrates

- Voice-agent pipeline design
- Separate STT, assistant, and TTS provider boundaries
- Conversation memory across turns
- Tool-style routing for common support intents
- Testable code instead of a one-off notebook
- Safe local defaults with no committed secrets

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

- `TranscriptFileSTT`: reads a text transcript as if it came from speech recognition
- `RuleBasedAssistant`: handles common support-style intents with deterministic logic
- `TextFileTTS`: writes the assistant response to a text artifact to stand in for synthesized audio

These interfaces can be replaced with real providers such as Whisper/faster-whisper for STT, Groq/OpenAI/local LLMs for reasoning, and ElevenLabs/XTTS/pyttsx3 for TTS.

## Quick Start

```bash
python -m voice_agent_demo.cli --transcript examples/sample_transcript.txt --output out/response.txt
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Example

Input transcript:

```text
My apartment wall has mold near the window. What should I do first?
```

Output:

```text
It sounds like a property maintenance issue...
```

## Project Structure

```text
.
|-- examples/
|   `-- sample_transcript.txt
|-- tests/
|   `-- test_pipeline.py
|-- voice_agent_demo/
|   |-- cli.py
|   |-- pipeline.py
|   `-- providers.py
|-- README.md
`-- requirements.txt
```

## Why This Matters

Voice AI systems fail when the audio pipeline, language model, and response layer are tangled together. This demo keeps them separate so latency, replacement providers, testing, and safety checks can be handled independently.

## Next Extensions

- Add `faster-whisper` STT adapter
- Add streaming TTS adapter
- Add latency logging per pipeline stage
- Add WebSocket or LiveKit transport
- Add evaluation tests for conversation quality

