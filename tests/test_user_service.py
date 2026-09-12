import pytest

from src.repositories.payment_repository import PaymentRepository
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


@pytest.fixture
def user_service() -> UserService:
    return UserService(UserRepository(), PaymentRepository())


def test_user_creation(user_service: UserService) -> None:
    user = user_service.create_user("Alice", "alice@example.com")

    assert user.id
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


def test_user_retrieval(user_service: UserService) -> None:
    created = user_service.create_user("Bob", "bob@example.com")

    fetched = user_service.get_user(created.id)

    assert fetched.id == created.id
    assert fetched.name == "Bob"
