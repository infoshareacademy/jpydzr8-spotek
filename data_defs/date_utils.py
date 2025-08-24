# data_defs/date_utils.py
from datetime import date, datetime
import re

_DOT_RE = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")

def ask_delivery_date_dot(
    prompt: str = "Data dostawy (DD.MM.RRRR): ",
    allow_past: bool = False,
    min_date: date | None = None,
    max_date: date | None = None,
) -> str:
    """
    Pyta o datę w formacie DD.MM.RRRR (z kropkami), waliduje istnienie daty i zakres.
    Zwraca sformatowane 'DD.MM.RRRR'.
    """
    while True:
        raw = input(prompt).strip()
        if not _DOT_RE.match(raw):
            print("⚠️  Wpisz datę w formacie DD.MM.RRRR (np. 05.09.2025).")
            continue
        try:
            d = datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("⚠️  Nieistniejąca data (np. 31.02). Spróbuj ponownie.")
            continue

        lo = min_date if min_date else (date.today() if not allow_past else None)
        hi = max_date
        if lo and d < lo:
            print(f"⚠️  Data nie może być wcześniejsza niż {lo.strftime('%d.%m.%Y')}.")
            continue
        if hi and d > hi:
            print(f"⚠️  Data nie może być późniejsza niż {hi.strftime('%d.%m.%Y')}.")
            continue
        return d.strftime("%d.%m.%Y")
