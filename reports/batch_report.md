# Voice Agent Batch Report

Scenarios: `6`
Intent accuracy: `1.0`

## Average Latency

| Stage | Avg ms | P50 ms | P95 ms | Max ms |
| --- | ---: | ---: | ---: | ---: |
| stt | 0.895 | 0.604 | 2.189 | 2.714 |
| assistant | 0.031 | 0.028 | 0.061 | 0.071 |
| tts | 2.114 | 1.034 | 5.71 | 6.95 |

## Event Counts

| Event | Count |
| --- | ---: |
| barge_in | 1 |
| silence | 1 |

## Safety Note Counts

| Note | Count |
| --- | ---: |
| barge_in_handled | 1 |
| emergency_escalation | 2 |
| jurisdiction_specific_advice | 1 |
| low_confidence_transcript | 1 |
| silence_detected | 1 |

## Scenario Results

### maintenance_mold

- Expected intent: property_maintenance
- Predicted intent: property_maintenance
- Confidence: 0.91
- Transcript confidence: 1.0
- Events: none
- Intent match: True
- Response artifact: `reports\maintenance_mold_response.txt`

### tenancy_notice

- Expected intent: tenancy_guidance
- Predicted intent: tenancy_guidance
- Confidence: 0.87
- Transcript confidence: 1.0
- Events: none
- Intent match: True
- Response artifact: `reports\tenancy_notice_response.txt`

### gas_emergency

- Expected intent: emergency_escalation
- Predicted intent: emergency_escalation
- Confidence: 0.94
- Transcript confidence: 1.0
- Events: none
- Intent match: True
- Response artifact: `reports\gas_emergency_response.txt`

### silence_timeout

- Expected intent: silence_timeout
- Predicted intent: silence_timeout
- Confidence: 0.98
- Transcript confidence: 1.0
- Events: silence
- Intent match: True
- Response artifact: `reports\silence_timeout_response.txt`

### low_confidence_wall

- Expected intent: clarification_request
- Predicted intent: clarification_request
- Confidence: 0.42
- Transcript confidence: 0.42
- Events: none
- Intent match: True
- Response artifact: `reports\low_confidence_wall_response.txt`

### barge_in_gas

- Expected intent: emergency_escalation
- Predicted intent: emergency_escalation
- Confidence: 0.94
- Transcript confidence: 1.0
- Events: barge_in
- Intent match: True
- Response artifact: `reports\barge_in_gas_response.txt`
