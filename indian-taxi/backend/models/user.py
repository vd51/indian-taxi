from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    role: str
    phone: str
    email: Optional[str]
    password_hash: str
    is_active: bool
    is_verified: bool

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            role=row["role"],
            phone=row["phone"],
            email=row["email"],
            password_hash=row["password_hash"],
            is_active=bool(row["is_active"]),
            is_verified=bool(row["is_verified"])
        )
