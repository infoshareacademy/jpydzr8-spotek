# delivery.py
import csv
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Delivery:
    id: int
    login: str
    company: str
    delivery_date: str
    delivery_type: str
    unit_type: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    # --- Pola opcjonalne ---
    driver_name: str = ""
    driver_phone: str = ""
    truck_no: str = ""
    trailer_no: str = ""
    order_no: str = ""
    attachment_name: str = ""
    attachment_size_bytes: str = ""
    attachment_path: str = ""

    def save_to_file(self, path: str) -> None:
        """Dopisuje pojedynczy rekord do pliku CSV (delimiter=';')."""
        with open(path, mode="a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([
                self.id,
                self.login,
                self.company,
                self.delivery_date,
                self.delivery_type,
                self.unit_type,
                self.created_at,
                self.driver_name,
                self.driver_phone,
                self.truck_no,
                self.trailer_no,
                self.order_no,
                self.attachment_name,
                self.attachment_size_bytes,
                self.attachment_path,
            ])
