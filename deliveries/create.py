import csv
import os
import shutil

def read_csv_options(path):
    try:
        with open(path, newline='', encoding='utf-8') as f:
            return [row[0] for row in csv.reader(f) if row and row[0].strip()]
    except UnicodeDecodeError:
        print("⚠️ Plik nie jest w UTF-8. Próbuję cp1250...")
        with open(path, newline='', encoding='cp1250') as f:
            return [row[0] for row in csv.reader(f) if row and row[0].strip()]

def save_attachment(source_path):
    if not os.path.isfile(source_path):
        print("❌ Podany plik nie istnieje.")
        return None

    os.makedirs("zalaczniki", exist_ok=True)
    filename = os.path.basename(source_path)
    destination_path = os.path.join("zalaczniki", filename)

    try:
        shutil.copy(source_path, destination_path)
        return destination_path
    except Exception as e:
        print(f"❌ Błąd przy zapisie załącznika: {e}")
        return None

def create_awizacja():
    print("\n=== ZAKŁADANIE AWIZACJI ===")
    # Typ dostawy
    types = read_csv_options("baza_danych/typ_dostawy_slownik.csv")
    print("Typy dostaw:", types)
    typ_dostawy = input("Wybierz typ: ")

    # Jednostki ładunkowe
    units = read_csv_options("baza_danych/typ_jednostki.csv")
    print("Jednostki ładunkowe:", units)
    jednostka = input("Wybierz jednostkę: ")

    # Daty dostaw
    dates = read_csv_options("baza_danych/daty_dostaw_slownik.csv")
    print("Dostępne daty:", dates)
    data = input("Wybierz datę dostawy: ")

    # Numer zamówienia
    nr_zamowienia = input("Numer zamówienia: ")

    print("\nCzy chcesz dodać załącznik? (t/n): ", end="")
    dodaj = input().strip().lower()

    saved_file = None

    if dodaj == 't':
        zalacznik_path = input("Ścieżka do pliku załącznika: ").strip()
        saved_file = save_attachment(zalacznik_path)

        if saved_file:
            print("✅ Załącznik został zapisany.")
        else:
            print("⚠️ Nie udało się zapisać załącznika.")
    elif dodaj != 'n':
        print("⚠️ Nieprawidłowa odpowiedź – pomijam dodanie załącznika.")

    # Podsumowanie
    print("\n=== PODSUMOWANIE AWIZACJI ===")
    print(f"✔️ Typ dostawy: {typ_dostawy}")
    print(f"✔️ Jednostka ładunkowa: {jednostka}")
    print(f"✔️ Data dostawy: {data}")
    print(f"✔️ Numer zamówienia: {nr_zamowienia}")
    if saved_file:
        print(f"✔️ Załącznik zapisany jako: {saved_file}")
    else:
        print("❌ Załącznik: brak")

    print("\n🎉 Awizacja została prawidłowo założona.")
