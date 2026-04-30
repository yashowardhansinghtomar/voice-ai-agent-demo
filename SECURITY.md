# Security

This repository is a local voice-agent architecture demo. It does not require API keys, live calls, microphones, or customer recordings.

## Data Handling

Do not commit:

- Real call transcripts.
- Customer audio.
- Phone numbers or personal data.
- API keys, tokens, or provider credentials.
- Private operational scripts.

Use synthetic transcripts for public examples.

## Voice-AI-Specific Risk

Production voice agents can handle sensitive personal information. This demo does not implement consent capture, call recording controls, authentication, telephony compliance, or production monitoring.

If adapting this for production, add:

- Consent and recording controls.
- Redaction for logs and traces.
- Provider timeout and retry policies.
- Safety escalation rules.
- Access controls for transcripts and recordings.

## Reporting Issues

If you find a security issue, open a private report through GitHub Security Advisories if available. If that is not available, contact the repository owner directly and avoid posting sensitive details in a public issue.
