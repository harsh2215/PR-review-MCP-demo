from __future__ import annotations

from typing import Dict, List, Optional

from src.models.payment import Payment


class PaymentRepository:
    def __init__(self) -> None:
        self._payments: Dict[str, Payment] = {}

    def save(self, payment: Payment) -> Payment:
        self._payments[payment.id] = payment
        return payment

    def find_by_id(self, payment_id: str) -> Optional[Payment]:
        return self._payments.get(payment_id)

    def find_all(self) -> List[Payment]:
        return list(self._payments.values())

    def update(self, payment: Payment) -> Payment:
        self._payments[payment.id] = payment
        return payment
