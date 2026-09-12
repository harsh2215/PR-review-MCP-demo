from __future__ import annotations

import uuid

from src.cache.cache_manager import CacheManager
from src.models.payment import Payment
from src.repositories.payment_repository import PaymentRepository


class PaymentNotFoundError(Exception):
    pass


class RetryLimitExceededError(Exception):
    pass


class PaymentService:
    def __init__(
        self, payment_repository: PaymentRepository, cache_manager: CacheManager[Payment]
    ) -> None:
        self._payment_repository = payment_repository
        self._cache_manager = cache_manager

    def create_payment(self, user_id: str, amount: float, currency: str) -> Payment:
        payment = Payment(
            id=str(uuid.uuid4()), user_id=user_id, amount=amount, currency=currency
        )
        self._payment_repository.save(payment)
        self._cache_manager.set(payment.id, payment)
        return payment

    def get_payment(self, payment_id: str) -> Payment:
        cached = self._cache_manager.get(payment_id)
        if cached:
            return cached

        payment = self._payment_repository.find_by_id(payment_id)
        if not payment:
            raise PaymentNotFoundError(f"Payment '{payment_id}' not found")

        self._cache_manager.set(payment_id, payment)
        return payment

    def update_payment_status(self, payment_id: str, status: str) -> Payment:
        payment = self.get_payment(payment_id)
        payment.status = status
        updated = self._payment_repository.update(payment)
        self._cache_manager.set(payment_id, updated)
        return updated

    def retry_payment(self, payment_id: str) -> Payment:
        payment = self.get_payment(payment_id)
        if payment.retry_count >= payment.max_retries:
            raise RetryLimitExceededError(
                f"Payment '{payment_id}' exceeded retry limit of {payment.max_retries}"
            )
        payment.retry_count += 1
        payment.status = "pending"
        updated = self._payment_repository.update(payment)
        self._cache_manager.set(payment_id, updated)
        return updated
