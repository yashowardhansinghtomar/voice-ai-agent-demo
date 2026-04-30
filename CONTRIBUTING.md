# Contributing

This project demonstrates voice-agent architecture without requiring API keys or audio hardware. Contributions should keep provider boundaries clear and local tests reliable.

## Local Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Before Opening A PR

- Run the unit tests.
- Run the sample transcript command.
- Run the batch scenario command.
- Add tests for new providers, routing behavior, or trace output.
- Keep real provider integrations optional.

## Good Contributions

- New local scenarios for appointment booking, support, escalation, or interruptions.
- Better latency trace summaries.
- Provider interface examples for real STT, LLM, or TTS services.
- Barge-in or silence-handling simulations.
- More precise batch evaluation metrics.

## Style

- Keep the default demo runnable without credentials.
- Keep STT, assistant, and TTS concerns separate.
- Make latency and behavior visible through traces and reports.
- Avoid committing generated audio or private call transcripts.
