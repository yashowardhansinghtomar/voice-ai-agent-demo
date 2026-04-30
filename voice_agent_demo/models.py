from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class StageTrace:
    stage: str
    latency_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationTurn:
    user: str
    assistant: str
    intent: str
    confidence: float


@dataclass
class AssistantResponse:
    text: str
    intent: str
    confidence: float
    safety_notes: list[str] = field(default_factory=list)


@dataclass
class TurnResult:
    user_text: str
    response_text: str
    intent: str
    confidence: float
    artifact_path: str
    turn_count: int
    traces: list[StageTrace]
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

