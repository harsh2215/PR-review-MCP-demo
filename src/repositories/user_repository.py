from __future__ import annotations

from typing import Dict, List, Optional

from src.models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def find_all(self) -> List[User]:
        return list(self._users.values())

    def update(self, user: User) -> User:
        self._users[user.id] = user
        return user
