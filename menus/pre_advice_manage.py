# menus/pre_advice_manage.py
import os
import csv
from .pre_advice_create import (
    ARCHIVE_PATH, ATTACH_DIR, MAX_ATTACH_BYTES, HEADERS,
    ensure_archive_and_header, pick_and_copy_attachment,
)
from data_defs.delivery_types import choose_delivery_type

try:
    from data_defs.hu_types import prompt_hu_quantities, to_compact_string
    ADV_HU = True
except Exception:
    from data_defs.hu_types import choose_hu_types
    ADV_HU = False

try:
    from data_defs.date_utils import ask_delivery_date as _ask_date
except Exception:
    _ask_date = None

# --- lokalne utilsy do CSV ---

def _load_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.reader(f, delimiter=";")
        try:
            header = next(r)
        except StopIteration:
            return [], []
        rows = [row for row in r]
    return header, rows

def _save_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if header:
            w.writerow(header)
        for row in rows:
            w.writerow(row)

def _col(header, name):
    try:
        return header.index(name)
    except ValueError:
        return None

def _remove_attachment_file(header, row):
    i_path = _col(header, "attachment_path")
    if i_path is None or i_path >= len(row):
        return
    p = row[i_path].strip()
    if p and os.path.isfile(p):
        try:
            os.remove(p)
        except Exception:
            pass

def _ask_delivery_date():
    if _ask_date:
        return _ask_date(allow_past=False)
    return input("Data dostawy (DD/MM/RRRR): ").strip()

def _input_optional(prompt: str) -> str:
    return input(prompt).strip()

def _input_phone_optional(prompt: str) -> str:
    raw = input(prompt).strip()
    if raw == "":
        return ""
    return raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace(".", "")

# --- operacje na rekordzie ---

def _edit_row_via_prompt(header, row):
    i_date      = _col(header, "delivery_date")
    i_type      = _col(header, "delivery_type")
    i_unit      = _col(header, "unit_type")
    i_dname     = _col(header, "driver_name")
    i_dphone    = _col(header, "driver_phone")
    i_truck     = _col(header, "truck_no")
    i_trailer   = _col(header, "trailer_no")
    i_order     = _col(header, "order_no")
    i_att_name  = _col(header, "attachment_name")
    i_att_size  = _col(header, "attachment_size_bytes")
    i_att_path  = _col(header, "attachment_path")
    i_id_col    = _col(header, "id")

    def get(idx): return row[idx] if idx is not None and idx < len(row) else ""

    while True:
        print("\n✏️  Co chcesz zmienić?")
        print(f"1. Data dostawy        [obecnie: {get(i_date) or '—'}]")
        print(f"2. Typ dostawy         [obecnie: {get(i_type) or '—'}]")
        print(f"3. Jednostki (HU)      [obecnie: {get(i_unit) or '—'}]")
        print(f"4. Imię i nazwisko     [obecnie: {get(i_dname) or '—'}]")
        print(f"5. Telefon kierowcy    [obecnie: {get(i_dphone) or '—'}]")
        print(f"6. Nr auta (ciągnik)   [obecnie: {get(i_truck) or '—'}]")
        print(f"7. Nr naczepy          [obecnie: {get(i_trailer) or '—'}]")
        print(f"8. Numer zamówienia    [obecnie: {get(i_order) or '—'}]")
        print(f"9. Załącznik           [obecnie: {get(i_att_name) or '—'}]")
        print("0. Zakończ edycję i zapisz")
        choice = input("Wybierz opcję: ").strip()

        if choice == "1" and i_date is not None:
            row[i_date] = _ask_delivery_date()
        elif choice == "2" and i_type is not None:
            row[i_type] = choose_delivery_type()
        elif choice == "3" and i_unit is not None:
            if ADV_HU:
                q = prompt_hu_quantities()
                row[i_unit] = to_compact_string(q)
            else:
                row[i_unit] = choose_hu_types()
        elif choice == "4" and i_dname is not None:
            row[i_dname] = _input_optional("Imię i nazwisko (Enter = puste): ")
        elif choice == "5" and i_dphone is not None:
            row[i_dphone] = _input_phone_optional("Telefon kierowcy (Enter = puste): ")
        elif choice == "6" and i_truck is not None:
            row[i_truck] = _input_optional("Nr auta (Enter = puste): ")
        elif choice == "7" and i_trailer is not None:
            row[i_trailer] = _input_optional("Nr naczepy (Enter = puste): ")
        elif choice == "8" and i_order is not None:
            row[i_order] = _input_optional("Numer zamówienia (Enter = puste): ")
        elif choice == "9" and i_att_name is not None:
            print("\nZałącznik: [P]odmień / [U]suń / Enter = nic")
            a = input("> ").strip().lower()
            if a in ("u", "usun", "usuń"):
                _remove_attachment_file(header, row)
                row[i_att_name] = ""
                if i_att_size is not None: row[i_att_size] = ""
                if i_att_path is not None: row[i_att_path] = ""
            elif a in ("p", "podmien", "podmień"):
                try:
                    _id = int(row[i_id_col]) if i_id_col is not None else 0
                except Exception:
                    _id = 0
                name, size, rel = pick_and_copy_attachment(_id, ATTACH_DIR, MAX_ATTACH_BYTES)
                if name:
                    _remove_attachment_file(header, row)
                    row[i_att_name] = name
                    if i_att_size is not None: row[i_att_size] = size
                    if i_att_path is not None: row[i_att_path] = rel
        elif choice == "0":
            break
        else:
            print("⚠️  Nieprawidłowa opcja.")
    return row

def _soft_delete_row(header, row):
    """Czyści dane, ale zostawia id, login, created_at; delivery_type = '(usunięta)'."""
    i_id      = _col(header, "id")
    i_login   = _col(header, "login")
    i_created = _col(header, "created_at")
    i_type    = _col(header, "delivery_type")

    _remove_attachment_file(header, row)

    for i in range(len(header)):
        if i in (i_id, i_login, i_created):
            continue
        if i == i_type:
            row[i] = "(usunięta)"
        else:
            row[i] = ""
    return row

# --- publiczna funkcja menu „Moje awizacje” ---

def handle_my_advices_menu(login: str, path: str, attach_dir: str, max_attach_bytes: int) -> None:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print("📭 Brak zapisanych awizacji.")
        return

    header, rows = _load_csv(path)
    if not header:
        print("📭 Plik jest pusty.")
        return

    i_login = _col(header, "login")
    i_id    = _col(header, "id")
    if i_login is None or i_id is None:
        print("⚠️  Brak wymaganych kolumn w pliku.")
        return

    me = (login or "").strip()
    my_rows = [row for row in rows if len(row) > i_login and row[i_login].strip() == me]
    if not my_rows:
        print("📭 Brak awizacji dla tego użytkownika.")
        return

    print("\n🗂️ Twoje awizacje:")
    print(" | ".join(h.strip() for h in header))
    for r in my_rows:
        print(" | ".join(c.strip() for c in r))

    action = input("\nCo chcesz zrobić? [E]dytuj / [U]suń / Enter = nic: ").strip().lower()
    if action not in ("e", "u", "edytuj", "usun", "usuń"):
        return

    sel = input("Podaj ID awizacji: ").strip()
    if not sel.isdigit():
        print("⚠️  ID musi być liczbą całkowitą.")
        return

    target_i = None
    for i, row in enumerate(rows):
        if len(row) > i_id and row[i_id] == sel:
            if len(row) > i_login and row[i_login].strip() == me:
                target_i = i
            break

    if target_i is None:
        print("⚠️  Nie znaleziono Twojej awizacji o tym ID.")
        return

    if action in ("u", "usun", "usuń"):
        confirm = input(f"Czy na pewno usunąć dane awizacji ID {sel} (ID pozostanie)? [t/N]: ").strip().lower()
        if confirm in ("t", "tak", "y", "yes"):
            rows[target_i] = _soft_delete_row(header, rows[target_i])
            _save_csv(path, header, rows)
            print("🗑️  Dane usunięte. ID pozostawione.")
        else:
            print("❎ Anulowano.")
    else:
        rows[target_i] = _edit_row_via_prompt(header, rows[target_i])
        _save_csv(path, header, rows)
        print("✅ Zapisano zmiany.")
