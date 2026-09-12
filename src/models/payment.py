from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Payment:
    id: str
    user_id: str
    amount: float
    currency: str
    status: str = "pending"
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
