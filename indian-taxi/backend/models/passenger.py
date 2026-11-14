from dataclasses import dataclass
from typing import Optional


@dataclass
class Passenger:
    id: str
    user_id: str
    full_name: str
    profile_photo: Optional[str]
    emergency_contact: Optional[str]

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            user_id=row["user_id"],
            full_name=row["full_name"],
            profile_photo=row["profile_photo"],
            emergency_contact=row["emergency_contact"]
        )
