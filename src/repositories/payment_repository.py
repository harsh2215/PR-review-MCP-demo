from __future__ import annotations

import threading
from typing import Dict, List, Optional

from src.models.payment import Payment


class PaymentRepository:
    def __init__(self) -> None:
        self._payments: Dict[str, Payment] = {}
        self._lock = threading.Lock()
        self._locks: Dict[str, threading.Lock] = {}

    def save(self, payment: Payment) -> Payment:
        self._payments[payment.id] = payment
        return payment

    def find_by_id(self, payment_id: str) -> Optional[Payment]:
        return self._payments.get(payment_id)

    def find_all(self) -> List[Payment]:
        return list(self._payments.values())

    def update(self, payment: Payment) -> Payment:
        with self._lock:
            self._payments[payment.id] = payment
            return payment

    def get_lock(self, payment_id: str) -> threading.Lock:
        with self._lock:
            if payment_id not in self._locks:
                self._locks[payment_id] = threading.Lock()
            return self._locks[payment_id]
