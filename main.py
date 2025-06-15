import csv
import os
#from datetime import datetime
from core.user_manager import UserManager
from core.delivery import Delivery

print("Witaj w Spotek\n")

um = UserManager("db/users.csv")
um.load_users()

# def validate_date(prompt):
#     while True:
#         date_str = input(prompt)
#         try:
#             datetime.strptime(date_str, "%d/%m/%Y")
#             return date_str
#         except ValueError:
#             print("❌ Niepoprawny format daty. Użyj formatu DD/MM/RRRR.")

def show_user_deliveries(login):
    print("\n📋 TWOJE AWIZACJE:")
    try:
        with open("archiwum/awizacje.csv", newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file, delimiter=';'))
            user_deliveries = []
            id_mapping = []
            for i, row in enumerate(reader):
                if row and row[1] == login or login == "admin":
                    dane = [elem if elem else "-" for elem in row]
                    display_id = len(user_deliveries)
                    print(f"\n🆔 ID: {dane[0]}\n📌 Zlecenie: {dane[7]}\n🗓 Data wysyłki: {dane[3]}\n📦 Data dostawy: {dane[4]}\n🚚 Typ: {dane[5]}\n📦 Jednostka: {dane[6]}\n👤 Kierowca: {dane[8]}\n🚛 Auto: {dane[9]}\n🛻 Naczepa: {dane[10]}\n📞 Telefon: {dane[11]}")
                    user_deliveries.append(row)
                    id_mapping.append(i)
            if user_deliveries:
                print("\nOpcje:")
                if login != "admin":
                    print("2. 🗑 Usuń awizację")
                if login == "admin":
                    print("4. 📜 Pokaż historię usuniętych awizacji")
                    print("5. 🗃 Pokaż kopię zapasową")
                print("3. 🔙 Powrót do menu")
                wybor = input("Wybierz opcję: ")
                if wybor == "2" and login != "admin":
                    try:
                        awizo_id = input("Podaj ID awizacji do usunięcia: ")
                        found = False
                        for idx, row in enumerate(reader):
                            if row and row[0] == awizo_id and row[1] == login:
                                true_id = idx
                                deleted_awizo = reader[true_id]

                                # Zapisz usunięte awizo do archiwum
                                os.makedirs("archiwum/historia", exist_ok=True)
                                with open("archiwum/historia/awizacje_historic.csv", mode='a', newline='', encoding='utf-8') as hist_file:
                                    writer = csv.writer(hist_file, delimiter=';')
                                    writer.writerow(deleted_awizo)

                                # Usuń z głównego pliku
                                reader.pop(true_id)
                                with open("archiwum/awizacje.csv", mode='w', newline='', encoding='utf-8') as file:
                                    writer = csv.writer(file, delimiter=';')
                                    writer.writerows(reader)
                                print(f"🗑 Awizacja ID {awizo_id} została usunięta i zapisana w historii.")
                                found = True
                                break
                        if not found:
                            print("❌ Nie znaleziono awizacji o podanym ID.")
                    except ValueError:
                        print("❌ Wprowadź poprawny numer ID.")
                elif wybor == "4" and login == "admin":
                    print("\n📜 HISTORIA USUNIĘTYCH AWIZACJI:")
                    try:
                        with open("archiwum/historia/awizacje_historic.csv", newline='', encoding='utf-8') as hist_file:
                            reader = csv.reader(hist_file, delimiter=';')
                            for row in reader:
                                dane = [elem if elem else "-" for elem in row]
                                print(f"\n🆔 ID: {dane[0]}\n📌 Zlecenie: {dane[7]}\n🗓 Data wysyłki: {dane[3]}\n📦 Data dostawy: {dane[4]}\n🚚 Typ: {dane[5]}\n📦 Jednostka: {dane[6]}\n👤 Kierowca: {dane[8]}\n🚛 Auto: {dane[9]}\n🛻 Naczepa: {dane[10]}\n📞 Telefon: {dane[11]}")
                    except FileNotFoundError:
                        print("❌ Brak pliku historii.")
                elif wybor == "5" and login == "admin":
                    print("\n🗃 KOPIA ZAPASOWA WSZYSTKICH AWIZACJI:")
                    try:
                        with open("archiwum/awizacje_backup.csv", newline='', encoding='utf-8') as backup_file:
                            reader = csv.reader(backup_file, delimiter=';')
                            for row in reader:
                                dane = [elem if elem else "-" for elem in row]
                                print(f"\n🆔 ID: {dane[0]}\n📌 Zlecenie: {dane[7]}\n🗓 Data wysyłki: {dane[3]}\n📦 Data dostawy: {dane[4]}\n🚚 Typ: {dane[5]}\n📦 Jednostka: {dane[6]}\n👤 Kierowca: {dane[8]}\n🚛 Auto: {dane[9]}\n🛻 Naczepa: {dane[10]}\n📞 Telefon: {dane[11]}")
                    except FileNotFoundError:
                        print("❌ Brak kopii zapasowej.")
                else:
                    print("Powrót do menu...")
    except FileNotFoundError:
        print("❌ Brak zapisanych awizacji.")

while True:
    print("\n📋 MENU GŁÓWNE")
    print("1. 🔐 Zaloguj się")
    print("2. 📝 Zarejestruj się")
    print("3. ❌ Wyjście")
    wybor = input("Wybierz opcję (1/2/3): ")

    if wybor == "1":
        login = input("Login: ")
        haslo = input("Hasło: ")
        if um.authenticate(login, haslo):
            print(f"✅ Zalogowano pomyślnie! Witaj, {login}")
            company = um.users[login]['kontrahent']

            while True:
                print("\n🧾 MENU UŻYTKOWNIKA")
                print("1. ➕ Dodaj awizację")
                print("2. 📄 Moje awizacje")
                print("3. 🔙 Wyloguj")
                wybor2 = input("Wybierz opcję: ")

                if wybor2 == "1":
                    print("\n📦 TWORZENIE NOWEJ AWIZACJI")
                    ship_date = input("Data wysyłki (DD/MM/RRRR): ")
                    delivery_date = input("Data dostawy (DD/MM/RRRR): ")
                    delivery_type = input("Typ dostawy: ")
                    unit_type = input("Typ jednostki: ")
                    order_number = input("Numer dokumentu zamówienia: ")
                    driver_name = input("Imię i nazwisko kierowcy (opcjonalnie): ")
                    vehicle_number = input("Nr auta (opcjonalnie): ")
                    trailer_number = input("Nr naczepy (opcjonalnie): ")
                    phone_number = input("Nr telefonu (opcjonalnie): ")

                    delivery_id = sum(1 for _ in open("archiwum/awizacje.csv", encoding='utf-8')) if os.path.exists("archiwum/awizacje.csv") else 0

                    delivery = Delivery(
                        id=delivery_id,
                        login=login,
                        company=company,
                        ship_date=ship_date,
                        delivery_date=delivery_date,
                        delivery_type=delivery_type,
                        unit_type=unit_type,
                        order_number=order_number,
                        driver_name=driver_name,
                        vehicle_number=vehicle_number,
                        trailer_number=trailer_number,
                        phone_number=phone_number
                    )

                    os.makedirs("archiwum", exist_ok=True)
                    delivery.save_to_file("archiwum/awizacje.csv")

                elif wybor2 == "2":
                    show_user_deliveries(login)

                elif wybor2 == "3":
                    print("👋 Wylogowano.")
                    break

                else:
                    print("⚠️ Nieprawidłowa opcja.")
        else:
            print("❌ Niepoprawny login lub hasło.")

    elif wybor == "2":
        login = input("Nowy login: ")
        haslo = input("Hasło: ")
        kontrahent = input("Kontrahent: ")
        um.register_user(login, haslo, kontrahent)

    elif wybor == "3":
        print("👋 Do zobaczenia!")
        break

    else:
        print("⚠️ Nieprawidłowa opcja. Spróbuj ponownie.")
