from __future__ import annotations
import os, sys
from typing import Optional

def _ensure_django() -> None:
    try:
        from django.conf import settings  # type: ignore
        if settings.configured:
            return
    except Exception:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yms.settings")
    import django  # type: ignore
    django.setup()

def list_pre_advices(limit: int = 20) -> None:
    _ensure_django()
    from dbcore.models import PreAdvice  # type: ignore
    rows = PreAdvice.objects.select_related("delivery_type").order_by("-delivery_date")[:limit]
    if not rows:
        print("⚠️ Brak awizacji.")
        return
    print(f"\n📋 Ostatnie {len(rows)} awizacje:")
    for r in rows:
        print(f"[{r.id}] {r.delivery_date} | {r.company} | {r.login} | {r.delivery_type or '-'} | {r.unit_type}")

def edit_pre_advice(preadvice_id: int) -> None:
    _ensure_django()
    from dbcore.models import PreAdvice  # type: ignore
    from core.pre_advice_create import _parse_date

    try:
        obj = PreAdvice.objects.get(id=preadvice_id)
    except PreAdvice.DoesNotExist:
        print(f"⚠️ Awizacja ID={preadvice_id} nie istnieje.")
        return

    print(f"\n✏️ Edycja awizacji {obj.id} ({obj.company}, {obj.delivery_date})")
    new_date = input(f"Nowa data [{obj.delivery_date}] (Enter = bez zmian): ").strip()
    if new_date:
        obj.delivery_date = _parse_date(new_date)

    new_driver = input(f"Kierowca [{obj.driver_name}] (Enter = bez zmian): ").strip()
    if new_driver:
        obj.driver_name = new_driver

    new_unit = input(f"Jednostki [{obj.unit_type}] (Enter = bez zmian): ").strip()
    if new_unit:
        obj.unit_type = new_unit

    obj.save()
    print("✅ Zapisano zmiany.")

def delete_pre_advice(preadvice_id: int) -> None:
    _ensure_django()
    from dbcore.models import PreAdvice  # type: ignore
    try:
        obj = PreAdvice.objects.get(id=preadvice_id)
    except PreAdvice.DoesNotExist:
        print(f"⚠️ Awizacja ID={preadvice_id} nie istnieje.")
        return
    confirm = input(f"Czy na pewno usunąć awizację {obj.id} ({obj.company}, {obj.delivery_date})? [t/N]: ").strip().lower()
    if confirm == "t":
        obj.delete()
        print("🗑️ Usunięto.")
    else:
        print("❌ Anulowano.")
