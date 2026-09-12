import pytest

from src.cache.cache_manager import CacheManager
from src.repositories.payment_repository import PaymentRepository
from src.services.payment_service import PaymentNotFoundError, PaymentService


@pytest.fixture
def payment_service() -> PaymentService:
    return PaymentService(PaymentRepository(), CacheManager())


def test_successful_payment_creation(payment_service: PaymentService) -> None:
    payment = payment_service.create_payment("user-1", 100.0, "USD")

    assert payment.id
    assert payment.user_id == "user-1"
    assert payment.amount == 100.0
    assert payment.currency == "USD"
    assert payment.status == "pending"


def test_payment_retrieval(payment_service: PaymentService) -> None:
    created = payment_service.create_payment("user-1", 50.0, "USD")

    retrieved = payment_service.get_payment(created.id)

    assert retrieved.id == created.id


def test_payment_status_update(payment_service: PaymentService) -> None:
    created = payment_service.create_payment("user-1", 20.0, "USD")

    updated = payment_service.update_payment_status(created.id, "completed")

    assert updated.status == "completed"


def test_invalid_payment_lookup(payment_service: PaymentService) -> None:
    with pytest.raises(PaymentNotFoundError):
        payment_service.get_payment("missing-payment")


def test_transfer_retry_state(payment_service: PaymentService) -> None:
    payment_a = payment_service.create_payment("user-1", 100.0, "USD")
    payment_b = payment_service.create_payment("user-2", 200.0, "USD")

    payment_service.transfer_retry_state(payment_a.id, payment_b.id)

    assert payment_a.retry_count == 1
    assert payment_b.retry_count == 1
