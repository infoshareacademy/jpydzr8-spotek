# menus/pre_advice_create.py
import os
import csv
import shutil
from datetime import datetime
from data_defs.delivery_types import choose_delivery_type

# HU: jeśli masz wersję z trzema ilościami → użyjemy jej; inaczej fallback
try:
    from data_defs.hu_types import prompt_hu_quantities, to_compact_string
    ADV_HU = True
except Exception:
    from data_defs.hu_types import choose_hu_types
    ADV_HU = False

# data z walidacją (jeśli masz data_defs/date_utils.py – użyjemy jej)
try:
    from data_defs.date_utils import ask_delivery_date_dot as _ask_date
except Exception:
    _ask_date = None

ARCHIVE_PATH = "archive/pre-advice.csv"
ATTACH_DIR = "archive/attachments"
MAX_ATTACH_BYTES = 10 * 1024 * 1024  # 10 MB

HEADERS = [
    "id",
    "login",
    "company",
    "delivery_date",
    "delivery_type",
    "unit_type",
    "created_at",
    "driver_name",
    "driver_phone",
    "truck_no",
    "trailer_no",
    "order_no",
    "attachment_name",
    "attachment_size_bytes",
    "attachment_path",
]

# --------- wspólne helpery (re-używane też przez pre_advice_manage.py) ---------

def ensure_archive_and_header(path=ARCHIVE_PATH, headers=HEADERS):
    """Tworzy/migruje CSV do aktualnego nagłówka (dopina brakujące kolumny na końcu)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter=";").writerow(headers)
        return

    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f, delimiter=";"))
    if not rows:
        with open(path, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter=";").writerow(headers)
        return

    old_header = rows[0]
    if old_header == headers:
        return

    if len(old_header) < len(headers):
        data = rows[1:]
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(headers)
            for row in data:
                row = row + [""] * (len(headers) - len(row))
                w.writerow(row)

def get_next_id(path=ARCHIVE_PATH) -> int:
    """Następne ID = (max istniejących id) + 1."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return 1
    max_id = 0
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.reader(f, delimiter=";")
        next(r, None)  # nagłówek
        for row in r:
            if not row:
                continue
            try:
                max_id = max(max_id, int(row[0]))
            except Exception:
                continue
    return max_id + 1

def _ask_delivery_date():
    if _ask_date:
        return _ask_date(allow_past=False)  # 'DD.MM.RRRR'
    # fallback awaryjny:
    import re, datetime as _dt
    _RE = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")
    while True:
        s = input("Data dostawy (DD.MM.RRRR): ").strip()
        if not _RE.match(s):
            print("⚠️  Format DD.MM.RRRR (np. 05.09.2025).")
            continue
        try:
            _dt.datetime.strptime(s, "%d.%m.%Y")
            return s
        except ValueError:
            print("⚠️  Nieistniejąca data.")

def _input_optional(prompt: str) -> str:
    return input(prompt).strip()

def _input_phone_optional(prompt: str) -> str:
    raw = input(prompt).strip()
    if raw == "":
        return ""
    return raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace(".", "")

def pick_and_copy_attachment(delivery_id: int, attach_dir: str = ATTACH_DIR, max_bytes: int = MAX_ATTACH_BYTES):
    """
    Popyta o ścieżkę pliku. Pusta → brak. Weryfikuje rozmiar ≤ max_bytes.
    Kopiuje do attach_dir z prefiksem ID. Zwraca (name, size_str, rel_path) albo ("", "", "").
    """
    os.makedirs(attach_dir, exist_ok=True)
    while True:
        p = input("Ścieżka do załącznika (<=10 MB, Enter aby pominąć): ").strip().strip('"')
        if p == "":
            return "", "", ""
        if not os.path.isfile(p):
            print("⚠️  Plik nie istnieje.")
            continue
        size = os.path.getsize(p)
        if size > max_bytes:
            print("⚠️  Załącznik przekracza 10 MB.")
            continue

        base = os.path.basename(p)
        target_name = f"{delivery_id:06d}__{base}"
        target_rel = os.path.join(attach_dir, target_name)
        try:
            shutil.copy2(p, target_rel)
            return base, str(size), target_rel.replace("\\", "/")
        except Exception as e:
            print(f"⚠️  Błąd kopiowania: {e}. Spróbuj ponownie lub Enter aby pominąć.")

# --------- właściwe tworzenie ---------

def create_pre_advice_quick_cli(login: str, company: str, Delivery) -> None:
    print("\n📦 TWORZENIE NOWEJ AWIZACJI")

    ensure_archive_and_header()

    # rezerwacja ID (potrzebny do nazwy pliku załącznika)
    delivery_id = get_next_id()
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    delivery_date = _ask_delivery_date()
    delivery_type = choose_delivery_type()

    if ADV_HU:
        q = prompt_hu_quantities()
        unit_type = to_compact_string(q)  # np. Paleta=1,5 | Karton=0 | Kontener=2
    else:
        unit_type = choose_hu_types()

    print("\n🚚 Dane kierowcy (Enter = pomiń):")
    driver_name  = _input_optional("   Imię i nazwisko: ")
    driver_phone = _input_phone_optional("   Telefon kierowcy: ")
    truck_no     = _input_optional("   Nr auta (ciągnik): ")
    trailer_no   = _input_optional("   Nr naczepy: ")

    print("\n🧾 Dane zamówienia (Enter = pomiń):")
    order_no = _input_optional("   Numer zamówienia: ")

    print("\n📎 Załącznik (opcjonalnie):")
    att_name, att_size, att_path = pick_and_copy_attachment(delivery_id)

    delivery = Delivery(
        id=delivery_id,
        login=login,
        company=company,
        delivery_date=delivery_date,
        delivery_type=delivery_type,
        unit_type=unit_type,
        created_at=created_at,
        driver_name=driver_name,
        driver_phone=driver_phone,
        truck_no=truck_no,
        trailer_no=trailer_no,
        order_no=order_no,
        attachment_name=att_name,
        attachment_size_bytes=att_size,
        attachment_path=att_path,
    )
    delivery.save_to_file(ARCHIVE_PATH)
    print("✅ Awizacja została zapisana!")
