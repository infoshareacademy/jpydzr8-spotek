import csv
import os
from django.conf import settings
from django.utils import timezone
from .models import Delivery

HEADERS = [
    "id","login","company","delivery_date","delivery_type","unit_type","created_at",
    "driver_name","driver_phone","truck_no","trailer_no","order_no",
    "attachment_name","attachment_size_bytes","attachment_path",
]

def _fmt_decimal_pl(v):
    s = format(v, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")

def _unit_type_str(d: Delivery):
    return (
        f"Paleta={_fmt_decimal_pl(d.hu_paleta)} | "
        f"Karton={_fmt_decimal_pl(d.hu_karton)} | "
        f"Kontener={_fmt_decimal_pl(d.hu_kontener)}"
    )

def export_csv(path=None):
    """
    Eksportuje WSZYSTKIE Delivery do CSV spójnego ze starą aplikacją CLI.
    Ścieżka domyślna: <BASE_DIR>/archive/pre-advice.csv
    """
    if path is None:
        path = settings.BASE_DIR / "archive" / "pre-advice.csv"

    # Utwórz folder 'archive' jeśli brak
    os.makedirs(path.parent, exist_ok=True)

    qs = Delivery.objects.all().order_by("id")

    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(HEADERS)
        for d in qs:
            created_local = timezone.localtime(d.created_at) if d.created_at else None

            att_name = att_size = att_path = ""
            if d.attachment:
                try:
                    att_name = os.path.basename(d.attachment.name)
                    att_size = str(d.attachment.size)
                    att_path = d.attachment.path.replace("\\", "/")
                except Exception:
                    pass

            w.writerow([
                d.id,
                d.user.username,
                d.company or "",
                d.delivery_date.strftime("%d.%m.%Y") if d.delivery_date else "",
                d.delivery_type or "",
                _unit_type_str(d),
                created_local.strftime("%d.%m.%Y %H:%M:%S") if created_local else "",
                d.driver_name or "",
                d.driver_phone or "",
                d.truck_no or "",
                d.trailer_no or "",
                d.order_no or "",
                att_name,
                att_size,
                att_path,
            ])
