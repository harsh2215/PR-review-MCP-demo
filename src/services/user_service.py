from __future__ import annotations

import uuid
from typing import Dict, List

from src.models.user import User
from src.repositories.payment_repository import PaymentRepository
from src.repositories.user_repository import UserRepository


class UserNotFoundError(Exception):
    pass


class UserService:
    def __init__(
        self, user_repository: UserRepository, payment_repository: PaymentRepository
    ) -> None:
        self._user_repository = user_repository
        self._payment_repository = payment_repository

    def create_user(self, name: str, email: str) -> User:
        user = User(id=str(uuid.uuid4()), name=name, email=email)
        return self._user_repository.save(user)

    def get_user(self, user_id: str) -> User:
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User '{user_id}' not found")
        return user

    def get_users_with_payments(self) -> List[Dict[str, object]]:
        users = self._user_repository.find_all()

        return [
            {
                "user": user,
                "payments": [
                payment
                for payment in self._payment_repository.find_all()
                if payment.user_id == user.id
            ],
        }
        for user in users
    ]
