# Voice Agent Batch Report

Scenarios: `3`
Intent accuracy: `1.0`

## Average Latency

| Stage | Latency ms |
| --- | ---: |
| stt | 0.158 |
| assistant | 0.012 |
| tts | 0.383 |

## Scenario Results

### maintenance_mold

- Expected intent: property_maintenance
- Predicted intent: property_maintenance
- Confidence: 0.91
- Intent match: True
- Response artifact: `reports\maintenance_mold_response.txt`

### tenancy_notice

- Expected intent: tenancy_guidance
- Predicted intent: tenancy_guidance
- Confidence: 0.87
- Intent match: True
- Response artifact: `reports\tenancy_notice_response.txt`

### gas_emergency

- Expected intent: emergency_escalation
- Predicted intent: emergency_escalation
- Confidence: 0.94
- Intent match: True
- Response artifact: `reports\gas_emergency_response.txt`
