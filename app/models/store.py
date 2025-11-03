from dataclasses import dataclass, field

@dataclass
class Message:
    role: str
    content: str
    timestamp: str

@dataclass
class SessionData:
    id: int
    session_user: str
    created_at: str

@dataclass
class DataStore:
    session: SessionData
    messages: list[Message] = field(default_factory=list)

SESSION_STORE: list[DataStore] = []
