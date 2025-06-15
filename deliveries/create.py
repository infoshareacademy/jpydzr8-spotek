import csv
import os
import shutil
from datetime import datetime

# === LOGOWANIE Z CSV ===

def read_users(path="baza_danych/uzytkownicy.csv"):
    users = {}
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')

            for row in reader:
                login = row.get("login", "").strip()
                haslo = row.get("haslo", "").strip()
                kontrahent = row.get("kontrahent", "").strip()
                if login:
                    if login not in users:
                        users[login] = []
                    users[login].append({"haslo": haslo, "kontrahent": kontrahent})
    except Exception as e:
        print(f"❌ Błąd wczytywania użytkowników: {e}")
    return users

def formularz_logowania_z_haslem():
    users = read_users()
    if not users:
        print("\u274c Brak danych u\u017cytkownik\u00f3w.")
        return None, None

    while True:
        login = input("\ud83d\udc64 Login: ").strip()
        haslo = input("\ud83d\udd11 Has\u0142o: ").strip()

        dane_lista = users.get(login)
        if dane_lista:
            for dane in dane_lista:
                if dane["haslo"] == haslo:
                    kontrahenci = [u["kontrahent"] for u in dane_lista if u["haslo"] == haslo]
                    if len(kontrahenci) > 1:
                        print("Dostępnych kontrahentów:")
                        for idx, k in enumerate(kontrahenci, start=1):
                            print(f"{idx}. {k}")
                        wybor = input("Wybierz numer kontrahenta: ").strip()
                        if wybor.isdigit() and 1 <= int(wybor) <= len(kontrahenci):
                            kontrahent = kontrahenci[int(wybor)-1]
                        else:
                            print("\u26a0\ufe0f Nieprawidłowy wybór kontrahenta.")
                            continue
                    else:
                        kontrahent = kontrahenci[0]
                    print(f"\u2714\ufe0f Zalogowano jako {login}. Przypisany kontrahent: {kontrahent}")
                    return login, kontrahent
        print("\u274c Nieprawidłowe dane logowania. Spróbuj ponownie.\n")

# === POMOCNICZE FUNKCJE ===

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

# === GŁÓWNA FUNKCJA ===

def create_awizacja():
    print("\n=== ZAKŁADANIE AWIZACJI ===")

    # Logowanie użytkownika
    user, kontrahent = formularz_logowania_z_bazy()
    if not user or not kontrahent:
        print("❌ Nie udało się przeprowadzić logowania.")
        return

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

    # Załącznik
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
    awizacja_id, plik_csv = zapisz_awizacje_jako_osobny_plik(user, kontrahent, typ_dostawy, jednostka, data, nr_zamowienia, saved_file)

    if awizacja_id:
        print(f"\n🆔 ID awizacji: {awizacja_id}")
        print(f"📄 Zapisano do pliku: archiwum/{plik_csv}")




    # Podsumowanie
    print("\n=== PODSUMOWANIE AWIZACJI ===")
    print(f"✔️ Użytkownik: {user}")
    print(f"✔️ Kontrahent: {kontrahent}")
    print(f"✔️ Typ dostawy: {typ_dostawy}")
    print(f"✔️ Jednostka ładunkowa: {jednostka}")
    print(f"✔️ Data dostawy: {data}")
    print(f"✔️ Numer zamówienia: {nr_zamowienia}")
    if saved_file:
        print(f"✔️ Załącznik zapisany jako: {saved_file}")
    else:
        print("❌ Załącznik: brak")

    print("\n🎉 Awizacja została prawidłowo założona.")

# --- Możesz odkomentować to na koniec:
# cr
