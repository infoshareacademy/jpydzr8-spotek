from __future__ import annotations

import sys
from datetime import datetime
from typing import Optional

from django.contrib.auth import authenticate
from django.db import transaction

# MODELE z dbcore (spójne z bazą)
from dbcore.models import (
    PreAdvice,
    Company,
    DeliveryType,
    HUType,
    PreAdviceHU,
)


# =============================
#   POMOCNICZE I/O
# =============================

def _input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Do zobaczenia!")
        sys.exit(0)


def _pause() -> None:
    _input("\n[Enter] – kontynuuj...")


def _parse_date(s: str) -> Optional[datetime.date]:
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def _print_preadvice_row(p: PreAdvice) -> None:
    print(
        f"[{p.id}] {p.date} | {p.company.name} | {p.delivery_type.Delivery_type} | {p.hu_summary} | "
        f"{p.driver_name or '-'} ({p.driver_lang or '-'}) | {p.vehicle_number or '-'} / {p.trailer_number or '-'} | "
        f"{p.order_number or '-'}"
    )


# =============================
#   START MENU
# =============================

def start_menu() -> None:
    while True:
        print("\n=== START ===")
        print("1. Rejestracja użytkownika")
        print("2. Logowanie użytkownika")
        print("0. Wyjście")
        choice = _input("Wybierz opcję: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                print(f"🔓 Użytkownik {user.username} poprawnie zalogowany.")
                main_menu(user)
        elif choice == "0":
            print("👋 Do zobaczenia!")
            sys.exit(0)
        else:
            print("❌ Niepoprawny wybór.")


def register_user() -> None:
    from django.contrib.auth.models import User

    print("\n=== REJESTRACJA ===")
    username = _input("Login: ")
    if not username:
        print("❌ Login jest wymagany.")
        return
    if User.objects.filter(username=username).exists():
        print("❌ Taki login już istnieje.")
        return
    password = _input("Hasło: ")
    if not password:
        print("❌ Hasło jest wymagane.")
        return
    email = _input("E-mail (opcjonalnie): ")

    user = User.objects.create_user(username=username, password=password, email=email or "")
    print(f"✅ Utworzono użytkownika: {user.username}")


def login_user():
    print("\n=== LOGOWANIE ===")
    username = _input("Login: ")
    password = _input("Hasło: ")
    user = authenticate(username=username, password=password)
    if not user:
        print("❌ Błędne dane logowania.")
        return None
    return user


# =============================
#   GŁÓWNE MENU
# =============================

def main_menu(user) -> None:
    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Dodaj awizację")
        print("2. Lista awizacji (z filtrami)")
        print("3. Edytuj awizację")
        print("4. Usuń awizację")
        print("0. Wyloguj i wróć do startu")
        choice = _input("\nWybierz opcję: ")

        if choice == "1":
            add_preadvice(user)
        elif choice == "2":
            list_preadvices(user)
        elif choice == "3":
            edit_preadvice(user)
        elif choice == "4":
            delete_preadvice(user)
        elif choice == "0":
            print("↩️ Wylogowano.\n")
            return
        else:
            print("❌ Niepoprawny wybór.")


# =============================
#   DOSTĘPNE AWIZACJE (scope)
# =============================

def _accessible_preadvices(user):
    """
    Zwraca queryset awizacji dostępnych dla zalogowanego użytkownika.
    W bazie kolumna 'login' to TEXT.
    """
    qs = (
        PreAdvice.objects.select_related("company", "delivery_type")
        .prefetch_related("hu_rows__hu_type")
        .all()
    )
    if not user.is_superuser:
        qs = qs.filter(login=user.username)  # TEXT
    return qs


# =============================
#   DODAJ AWIZACJĘ
# =============================

def add_preadvice(user) -> None:
    print("\n=== DODAJ AWIZACJĘ ===")

    companies = list(Company.objects.all())
    if not companies:
        print("❌ Brak firm w systemie. Dodaj firmę w panelu admina.")
        return

    print("\nDostępne firmy:")
    for idx, c in enumerate(companies, start=1):
        print(f"[{idx}] {c.name}")
    try:
        ci = int(_input("Wybierz numer firmy: "))
        company = companies[ci - 1]
    except Exception:
        print("❌ Niepoprawny wybór firmy.")
        return

    while True:
        ds = _input("Data dostawy (YYYY-MM-DD): ")
        d = _parse_date(ds)
        if d:
            break
        print("❌ Niepoprawny format daty.")

    dts = list(DeliveryType.objects.all())
    if not dts:
        print("❌ Brak typów dostawy w systemie.")
        return

    print("\nTypy dostawy:")
    for idx, t in enumerate(dts, start=1):
        print(f"[{idx}] {t.Delivery_type}")
    try:
        dti = int(_input("Wybierz numer typu dostawy: "))
        delivery_type = dts[dti - 1]
    except Exception:
        print("❌ Niepoprawny wybór typu dostawy.")
        return

    hus = list(HUType.objects.all())
    if not hus:
        print("❌ Brak zdefiniowanych jednostek HU w systemie.")
        return

    hu_rows = []
    while True:
        print("\nJednostki (HU):")
        for idx, h in enumerate(hus, start=1):
            print(f"[{idx}] {h.HU_type}")
        try:
            hi = int(_input("Wybierz numer HU: "))
            hu = hus[hi - 1]
        except Exception:
            print("❌ Niepoprawny wybór HU.")
            continue

        try:
            qty = int(_input(f"Podaj ilość dla {hu.HU_type}: "))
            if qty <= 0:
                raise ValueError()
        except Exception:
            print("❌ Ilość musi być dodatnią liczbą całkowitą.")
            continue

        hu_rows.append((hu, qty))
        more = _input("Czy chcesz dodać kolejny typ HU? (t/n): ").lower()
        if more != "t":
            if not hu_rows:
                print("❌ Musisz dodać co najmniej jedną pozycję HU.")
                continue
            break

    driver_name = _input("Imię i nazwisko kierowcy (Enter = pomiń): ")
    driver_phone = _input("Telefon kierowcy (Enter = pomiń): ")
    driver_lang = _input("Język komunikacji (np. PL, EN; Enter = pomiń): ").upper() or None
    vehicle_number = _input("Numer auta (Enter = pomiń): ")
    trailer_number = _input("Numer naczepy (Enter = pomiń): ")
    order_number = _input("Numer zamówienia (Enter = pomiń): ")

    with transaction.atomic():
        p = PreAdvice.objects.create(
            date=d,
            company=company,
            delivery_type=delivery_type,
            login=user.username,  # TEXT w bazie
            driver_name=driver_name or None,
            driver_phone=driver_phone or None,
            driver_lang=driver_lang or None,
            vehicle_number=vehicle_number or None,
            trailer_number=trailer_number or None,
            order_number=order_number or None,
        )
        for hu, qty in hu_rows:
            PreAdviceHU.objects.create(preadvice=p, hu_type=hu, quantity=qty)

    print(f"\n✅ Awizacja dodana: [{p.id}] {p.date} / {company.name} / {user.username}")


# =============================
#   LISTA AWIZACJI (z filtrami)
# =============================

def list_preadvices(user) -> None:
    print("\n=== LISTA AWIZACJI ===")

    date_from = _parse_date(_input("Filtr: data od (YYYY-MM-DD, Enter = pomiń): "))
    date_to = _parse_date(_input("Filtr: data do (YYYY-MM-DD, Enter = pomiń): "))

    qs = _accessible_preadvices(user)

    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    qs = qs.order_by("-date", "-id")

    if not qs.exists():
        print("Brak awizacji dla podanych filtrów.")
        _pause()
        return

    print("\nID\tData\t\tFirma\t\tLogin\tTyp dostawy\tHU\tKierowca (lang)\tAuto/Naczepa\tZamówienie")
    for p in qs:
        print(
            f"{p.id}\t{p.date}\t{p.company.name}\t{p.login}\t{p.delivery_type.Delivery_type}\t"
            f"{p.hu_summary}\t{(p.driver_name or '-')}"
            f" ({p.driver_lang or '-'})\t{p.vehicle_number or '-'}/{p.trailer_number or '-'}\t{p.order_number or '-'}"
        )
    _pause()


# =============================
#   EDYTUJ / USUŃ
# =============================

def _get_owned_queryset(user):
    return _accessible_preadvices(user)


def edit_preadvice(user) -> None:
    qs = _get_owned_queryset(user).order_by("-date", "-id")
    if not qs.exists():
        print("Brak awizacji do edycji.")
        _pause()
        return

    print("\n📦 Wybierz awizację do edycji:")
    for p in qs[:50]:
        _print_preadvice_row(p)

    try:
        pid = int(_input("Podaj ID awizacji: "))
    except Exception:
        print("❌ Niepoprawne ID.")
        return

    try:
        p = qs.get(pk=pid)
    except PreAdvice.DoesNotExist:
        print("❌ Awizacja nie istnieje lub brak uprawnień.")
        return

    while True:
        print(
            "\nCo chcesz edytować?\n"
            "1. Datę dostawy\n"
            "2. Typ dostawy\n"
            "3. Jednostki HU (+ ilości)\n"
            "4. Kierowcę (imię i tel.)\n"
            "5. Pojazd (auto/naczepa)\n"
            "6. Numer zamówienia\n"
            "0. Zapisz i wyjdź"
        )
        c = _input("Wybierz opcję: ")

        if c == "1":
            ds = _input("Nowa data (YYYY-MM-DD): ")
            nd = _parse_date(ds)
            if not nd:
                print("❌ Niepoprawny format daty.")
            else:
                p.date = nd
        elif c == "2":
            dts = list(DeliveryType.objects.all())
            for idx, t in enumerate(dts, start=1):
                print(f"[{idx}] {t.Delivery_type}")
            try:
                dti = int(_input("Wybierz numer typu dostawy: "))
                p.delivery_type = dts[dti - 1]
            except Exception:
                print("❌ Niepoprawny wybór.")
        elif c == "3":
            rows = list(p.hu_rows.select_related("hu_type").all())
            print("\nAktualne HU:")
            if rows:
                for r in rows:
                    print(f"- {r.hu_type.HU_type} = {r.quantity} (id wiersza: {r.id})")
            else:
                print("- brak")

            print("\nCo chcesz zrobić?")
            print("a) dodać/zmienić HU")
            print("b) usunąć HU")
            sub = _input("Wybór (a/b): ").lower()

            if sub == "a":
                hus = list(HUType.objects.all())
                for idx, h in enumerate(hus, start=1):
                    print(f"[{idx}] {h.HU_type}")
                try:
                    hi = int(_input("Wybierz HU: "))
                    hu = hus[hi - 1]
                except Exception:
                    print("❌ Niepoprawny wybór HU.")
                    continue
                try:
                    qty = int(_input(f"Ilość dla {hu.HU_type}: "))
                    if qty <= 0:
                        raise ValueError()
                except Exception:
                    print("❌ Ilość musi być > 0.")
                    continue
                PreAdviceHU.objects.update_or_create(
                    preadvice=p, hu_type=hu, defaults={"quantity": qty}
                )
                print("✅ Zapisano pozycję HU.")
            elif sub == "b":
                try:
                    rid = int(_input("Podaj ID wiersza HU do usunięcia: "))
                    PreAdviceHU.objects.filter(preadvice=p, id=rid).delete()
                    print("🗑️ Usunięto pozycję HU.")
                except Exception:
                    print("❌ Błędne ID.")
            else:
                print("❌ Nieznana opcja.")
        elif c == "4":
            p.driver_name = _input("Imię i nazwisko kierowcy (Enter = bez zmian): ") or p.driver_name
            p.driver_phone = _input("Telefon kierowcy (Enter = bez zmian): ") or p.driver_phone
            lang = _input("Język kierowcy (PL/EN/UA/DE... Enter = bez zmian): ").upper().strip()
            if lang:
                p.driver_lang = lang
        elif c == "5":
            p.vehicle_number = _input("Numer auta (Enter = bez zmian): ") or p.vehicle_number
            p.trailer_number = _input("Numer naczepy (Enter = bez zmian): ") or p.trailer_number
        elif c == "6":
            p.order_number = _input("Numer zamówienia (Enter = bez zmian): ") or p.order_number
        elif c == "0":
            p.save()
            print("✅ Zapisano zmiany.")
            break
        else:
            print("❌ Nieznana opcja.")


def delete_preadvice(user) -> None:
    qs = _get_owned_queryset(user).order_by("-date", "-id")
    if not qs.exists():
        print("Brak awizacji do usunięcia.")
        _pause()
        return

    print("\n📦 Wybierz awizację do usunięcia:")
    for p in qs[:50]:
        _print_preadvice_row(p)

    try:
        pid = int(_input("Podaj ID awizacji: "))
    except Exception:
        print("❌ Niepoprawne ID.")
        return

    try:
        p = qs.get(pk=pid)
    except PreAdvice.DoesNotExist:
        print("❌ Awizacja nie istnieje lub brak uprawnień.")
        return

    confirm = _input(f"Czy na pewno usunąć [{p.id}]? (tak/nie): ").lower()
    if confirm == "tak":
        p.delete()
        print("🗑️ Usunięto awizację.")
    else:
        print("Anulowano.")
