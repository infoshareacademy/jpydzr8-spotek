from __future__ import annotations
import os, sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Tuple, List

ATTACH_DIR = Path("media/attachments")
MAX_ATTACH_BYTES = 10 * 1024 * 1024  # 10 MB

def _ensure_django() -> None:
    try:
        from django.conf import settings  # type: ignore
        if settings.configured:
            return
    except Exception:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yms.settings")
    try:
        import django  # type: ignore
        django.setup()
    except Exception as e:
        print("⚠️ Nie udało się zainicjalizować Django:", e, file=sys.stderr)

def _parse_date(s: str) -> date:
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError("Niepoprawny format daty (użyj YYYY-MM-DD lub DD.MM.YYYY).")

def _delivery_types() -> List[tuple[int, str]]:
    from dbcore.models import DeliveryType  # type: ignore
    return list(DeliveryType.objects.values_list("id", "Delivery_type"))

def _choose_delivery_type() -> Optional[int]:
    types = _delivery_types()
    if not types:
        print("⚠️ Brak typów dostawy w bazie.")
        return None
    print("\nDostępne typy dostawy:")
    for tid, name in types:
        print(f"  [{tid}] {name}")
    raw = input("Wybierz ID (Enter = brak): ").strip()
    if not raw:
        return None
    if not raw.isdigit():
        print("⚠️ Podaj numer ID.")
        return _choose_delivery_type()
    tid = int(raw)
    if not any(tid == x for x, _ in types):
        print("⚠️ Nie ma takiego ID.")
        return _choose_delivery_type()
    return tid

def _attachment_meta(path_str: str) -> tuple[str, Optional[int], str]:
    p = Path(path_str).expanduser()
    if not p.exists():
        return (p.name, None, str(p))
    size = p.stat().st_size
    if size > MAX_ATTACH_BYTES:
        print(f"⚠️ Załącznik > {MAX_ATTACH_BYTES} B – zapisuję tylko metadane.")
    return (p.name, size, str(p))

def create_pre_advice(login: str, company: str) -> None:
    """Interaktywne tworzenie awizacji – zapis do DB."""
    _ensure_django()
    from dbcore.models import PreAdvice, DeliveryType  # type: ignore

    print("\n➕ Dodawanie awizacji (DB)")
    try:
        d_str = input("Data dostawy (YYYY-MM-DD / DD.MM.YYYY): ").strip()
        delivery_date = _parse_date(d_str)

        dt_id = _choose_delivery_type()
        dt_obj = None
        if dt_id:
            try:
                dt_obj = DeliveryType.objects.get(id=dt_id)
            except DeliveryType.DoesNotExist:
                print("⚠️ Brak wybranego typu – pominę.")
                dt_obj = None

        unit_type = input("Jednostki (np. 'Paleta=2 | Kontener=1'): ").strip()
        driver_name = input("Kierowca (imię i nazwisko): ").strip()
        driver_phone = input("Telefon kierowcy: ").strip()
        truck_no = input("Nr ciężarówki: ").strip()
        trailer_no = input("Nr naczepy: ").strip()
        order_no = input("Nr zamówienia: ").strip()

        attach_path = input("Ścieżka do załącznika (Enter = brak): ").strip()
        a_name, a_size, a_path = ("", None, "")
        if attach_path:
            a_name, a_size, a_path = _attachment_meta(attach_path)

        obj = PreAdvice.objects.create(
            login=login,
            company=company,
            delivery_date=delivery_date,
            delivery_type=dt_obj,
            unit_type=unit_type,
            driver_name=driver_name,
            driver_phone=driver_phone,
            truck_no=truck_no,
            trailer_no=trailer_no,
            order_no=order_no,
            attachment_name=a_name,
            attachment_size_bytes=a_size,
            attachment_path=a_path,
        )
        print(f"✅ Zapisano awizację ID={obj.id} dla {company} na {delivery_date}")
    except Exception as e:
        print("❌ Błąd:", e)
