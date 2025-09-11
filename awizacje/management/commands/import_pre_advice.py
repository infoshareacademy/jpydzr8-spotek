## -*- coding: utf-8 -*-
import csv
import os
import re
import datetime
from decimal import Decimal
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from awizacje.models import Delivery

User = get_user_model()
DEC_RE = re.compile(r"[-+]?\d+(?:[.,]\d+)?")

def parse_decimal_loose(s: str) -> Decimal:
    s = (s or "").strip().replace("\u00a0","").replace(" ","")
    if s == "":
        return Decimal("0")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return Decimal(s)

def parse_units(unit_str: str):
    pal = kart = kon = Decimal("0")
    if unit_str:
        try:
            for part in unit_str.split("|"):
                p = part.strip()
                if p.lower().startswith("paleta"):
                    pal = parse_decimal_loose(p.split("=",1)[1])
                elif p.lower().startswith("karton"):
                    kart = parse_decimal_loose(p.split("=",1)[1])
                elif p.lower().startswith("kontener"):
                    kon = parse_decimal_loose(p.split("=",1)[1])
        except Exception:
            pass
    return pal, kart, kon

def parse_any_datetime(s: str):
    """Obsługa wielu formatów: daty i daty z czasem; zwraca aware datetime lub None."""
    s = (s or "").strip()
    if not s:
        return None
    fmts = [
        # data
        "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%y", "%d/%m/%y", "%Y.%m.%d", "%Y/%m/%d",
        # data+czas
        "%d.%m.%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y.%m.%d %H:%M:%S",
        "%d.%m.%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M", "%Y.%m.%d %H:%M",
    ]
    for fmt in fmts:
        try:
            dt = datetime.datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = timezone.make_aware(dt)
            return dt
        except Exception:
            continue
    return None

class Command(BaseCommand):
    help = "Importuje awizacje z CSV (archive/pre-advice.csv) do bazy Delivery."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=str(settings.BASE_DIR / "archive" / "pre-advice.csv"),
            help="Ścieżka do pliku CSV z awizacjami.",
        )
        parser.add_argument(
            "--default-user",
            default=None,
            help="Login użytkownika, do którego przypisać rekordy, gdy login z CSV nie istnieje.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Nie zapisuj do bazy – tylko pokaż podsumowanie.",
        )

    def handle(self, *args, **opts):
        path = Path(opts["path"])
        default_user = opts["default_user"]
        dry = bool(opts["dry_run"])

        if not path.is_file():
            raise CommandError(f"Nie znaleziono pliku: {path}")

        fallback_user = None
        if default_user:
            U = get_user_model()
            try:
                fallback_user = U.objects.get(username=default_user)
            except U.DoesNotExist:
                raise CommandError(f"Użytkownik default-user={default_user!r} nie istnieje.")

        with path.open(encoding="utf-8", newline="") as f:
            r = csv.reader(f, delimiter=";")
            try:
                header = [h.strip() for h in next(r)]
            except StopIteration:
                self.stdout.write(self.style.WARNING("Plik CSV jest pusty."))
                return
            rows = [row for row in r]

        def col(name):
            try: return header.index(name)
            except ValueError: return None

        idx = {
            "id": col("id"),
            "login": col("login"),
            "company": col("company"),
            "delivery_date": col("delivery_date"),
            "delivery_type": col("delivery_type"),
            "unit_type": col("unit_type"),
            "created_at": col("created_at"),
            "driver_name": col("driver_name"),
            "driver_phone": col("driver_phone"),
            "truck_no": col("truck_no"),
            "trailer_no": col("trailer_no"),
            "order_no": col("order_no"),
            "attachment_name": col("attachment_name"),
            "attachment_size_bytes": col("attachment_size_bytes"),
            "attachment_path": col("attachment_path"),
        }

        imported = updated = skipped = 0
        os.environ["AWIZACJE_DISABLE_EXPORT"] = "1"  # wyłącz eksport na czas importu

        for row in rows:
            if not row:
                continue

            # ID (spróbuj zachować PK)
            pk = None
            if idx["id"] is not None:
                try:
                    pk = int((row[idx["id"]] or "").strip())
                except Exception:
                    pk = None

            # Użytkownik
            username = (row[idx["login"]] if idx["login"] is not None else "").strip()
            user = User.objects.filter(username=username).first() if username else None
            if not user:
                user = fallback_user or User.objects.filter(is_superuser=True).first()
                if not user:
                    self.stdout.write(self.style.WARNING(
                        f"Pomijam ID={pk}: brak użytkownika {username!r} i fallbacku/superusera."
                    ))
                    skipped += 1
                    continue

            # Pola podstawowe
            company   = (row[idx["company"]] if idx["company"] is not None else "").strip()
            ddate_raw = (row[idx["delivery_date"]] if idx["delivery_date"] is not None else "").strip()
            dtype     = (row[idx["delivery_type"]] if idx["delivery_type"] is not None else "").strip()
            unit_str  = (row[idx["unit_type"]] if idx["unit_type"] is not None else "").strip()

            # created_at (opcjonalnie; jeśli poprawne, użyjemy jako fallback dla delivery_date)
            created_dt = None
            if idx["created_at"] is not None:
                created_raw = (row[idx["created_at"]] or "").strip()
                created_dt = parse_any_datetime(created_raw)

            # delivery_date — spróbuj wiele formatów; jeśli nie wyjdzie, użyj created_at.date() lub dzisiejszej
            ddate_dt = parse_any_datetime(ddate_raw)
            if ddate_dt is not None:
                ddate = ddate_dt.date()
            else:
                ddate = created_dt.date() if created_dt else timezone.localdate()

            pal, kart, kon = parse_units(unit_str)

            # Dodatkowe
            driver_name  = (row[idx["driver_name"]]  if idx["driver_name"]  is not None else "").strip()
            driver_phone = (row[idx["driver_phone"]] if idx["driver_phone"] is not None else "").strip()
            truck_no     = (row[idx["truck_no"]]     if idx["truck_no"]     is not None else "").strip()
            trailer_no   = (row[idx["trailer_no"]]   if idx["trailer_no"]   is not None else "").strip()
            order_no     = (row[idx["order_no"]]     if idx["order_no"]     is not None else "").strip()

            # Utwórz / aktualizuj
            if pk and Delivery.objects.filter(pk=pk).exists():
                d = Delivery.objects.get(pk=pk); action = "update"
            else:
                d = Delivery(pk=pk) if pk else Delivery(); action = "create"

            d.user = user
            d.company = company
            d.delivery_date = ddate
            d.delivery_type = dtype or "(brak)"
            d.hu_paleta = pal
            d.hu_karton = kart
            d.hu_kontener = kon
            d.driver_name = driver_name
            d.driver_phone = driver_phone
            d.truck_no = truck_no
            d.trailer_no = trailer_no
            d.order_no = order_no

            if not dry:
                d.save()
                # Załącznik (opcjonalnie, jeśli istnieje i ≤10MB)
                if idx["attachment_path"] is not None:
                    apath = (row[idx["attachment_path"]] or "").strip().replace("\\", "/")
                    if apath and os.path.isfile(apath):
                        try:
                            if os.path.getsize(apath) <= 10 * 1024 * 1024:
                                from django.core.files import File
                                name = os.path.basename(apath)
                                with open(apath, "rb") as fh:
                                    d.attachment.save(name, File(fh), save=True)
                        except Exception:
                            pass

            imported += 1 if action == "create" else 0
            updated  += 1 if action == "update" else 0

        os.environ.pop("AWIZACJE_DISABLE_EXPORT", None)
        self.stdout.write(self.style.SUCCESS(
            f"Zakończono: imported={imported}, updated={updated}, skipped={skipped}, dry_run={dry}"
        ))
