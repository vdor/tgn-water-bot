import hashlib
from dataclasses import asdict, dataclass


@dataclass
class WaterIssue:
    date_text: str
    content: str
    is_sent_telegram: bool = False

    @classmethod
    def create_from_dict(cls, data: dict) -> "WaterIssue":
        return cls(
            date_text=data.get("date_text", ""),
            content=data.get("content", ""),
            is_sent_telegram=data.get("is_sent_telegram", False),
        )

    @property
    def hash(self):
        hash_object = hashlib.sha256((self.date_text + self.content).encode("utf-8"))
        return hash_object.hexdigest()

    @property
    def formatted(self) -> str:
        return f"{self.date_text}\n\n{self.content}"

    @property
    def asdict(self) -> dict:
        return asdict(self)
