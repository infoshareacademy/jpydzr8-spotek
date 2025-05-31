
import csv

def read_csv_options(path):
    try:
        with open(path, newline='', encoding='utf-8') as f:
            return [row[0] for row in csv.reader(f)]
    except UnicodeDecodeError:
        print("⚠️ Plik nie jest w UTF-8. Próbuję cp1250...")
        with open(path, newline='', encoding='cp1250') as f:
            return [row[0] for row in csv.reader(f)]


def create_awizacja():
    print("\n=== ZAKŁADANIE AWIZACJI ===")
    # Typ dostawy
    types = read_csv_options("baza_danych/typ_dostawy_slownik.csv")
    print("Typy dostaw:", types)
    typ = input("Wybierz typ: ")

    # Jednostki ładunkowe
    units = read_csv_options("baza_danych/typ_jednostki.csv")
    print("Jednostki ładunkowe:", units)
    jednostka = input("Wybierz jednostkę: ")

    # Daty dostaw
    dates = read_csv_options("baza_danych/delivery_dates.csv")
    print("Dostępne daty:", dates)
    data = input("Wybierz datę dostawy: ")

    # Numer zamówienia
    numer = input("Numer zamówienia: ")

    # Załącznik
    zalacznik_path = input("Ścieżka do pliku załącznika: ")
    saved_file = save_attachment(zalacznik_path)

    print(f"\n📦 Awizacja zapisana:")
    print(f"Typ: {typ}, Jednostka: {jednostka}, Data: {data}, Nr zamówienia: {numer}")
    print(f"Załącznik zapisany jako: {saved_file}")
