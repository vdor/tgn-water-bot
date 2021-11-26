import hashlib
from dataclasses import asdict, dataclass


@dataclass
class ElectricityIssue:
    start_off_date_text: str
    start_off_time_text: str

    start_on_date_text: str
    start_on_time_text: str

    place: str

    @classmethod
    def create_from_dict(cls, data: dict) -> "ElectricityIssue":
        return cls(
            start_off_date_text=data.get("start_off_date_text", ""),
            start_off_time_text=data.get("start_off_time_text", ""),
            start_on_date_text=data.get("start_on_time_text", ""),
            start_on_time_text=data.get("start_on_time_text", ""),
            place=data.get("place", ""),
        )

    @property
    def hash(self):
        s = self.start_off_date_text + self.start_off_time_text + self.place
        hash_object = hashlib.sha256(s.encode("utf-8"))
        return hash_object.hexdigest()

    @property
    def formatted(self) -> str:
        if self.start_off_date_text == self.start_on_date_text:
            head = self.start_off_date_text
        else:
            head = f"{self.start_off_date_text} - {self.start_on_date_text}"

        return (
            f"{head}\n\nОтключение электроенергии "
            f"с {self.start_off_time_text} до {self.start_on_time_text}"
            f"по адресам, ограниченным улицами и переулками:\n\n{self.place}"
        )

    @property
    def asdict(self) -> dict:
        return asdict(self)

    @property
    def is_empty(self) -> bool:
        return len(self.place) == 0
