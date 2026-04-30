# Roadmap

This roadmap shows how the project can mature from a local architecture demo into a more production-like voice AI prototype.

## Done

- Separate STT, assistant, and TTS provider boundaries.
- Local transcript-based STT provider.
- Rule-based assistant provider.
- Text artifact TTS provider.
- Streaming-style text artifact mode.
- Per-stage latency traces.
- Silence timeout handling.
- Low-confidence transcript clarification.
- Simulated barge-in / interruption handling.
- Batch scenario evaluation.
- p50/p95 latency summaries.
- Event and safety-note counts.
- Markdown and JSON reports.
- Unit-tested CLI.

## Next Improvements

1. Add optional real STT provider example behind an interface.
2. Add optional real TTS provider example behind an interface.
3. Add websocket or LiveKit-style transport simulation.
4. Add scenario evaluation for multi-turn appointment booking.
5. Add retry and timeout policy examples for provider failures.

## Production Direction

- Add websocket or LiveKit-style streaming transport.
- Add provider credentials through environment variables.
- Persist conversation state and traces.
- Add retry, timeout, and fallback policies.
- Add safety escalation rules and human handoff hooks.
- Add privacy controls for transcripts and recordings.

## Non-Goals

- Pretending local text files are full production audio.
- Requiring paid provider credentials to run the demo.
- Hiding latency inside a single end-to-end number.
