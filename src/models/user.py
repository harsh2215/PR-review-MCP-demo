from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
