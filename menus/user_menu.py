# user_menu.py
import os
import csv

def run_user_menu(login, company, Delivery):
    while True:
        print("\n🧾 MENU UŻYTKOWNIKA")
        print("1. ➕ Dodaj awizację")
        print("2. 📄 Moje awizacje (TODO)")
        print("3. 🔙 Wyloguj")
        wybor2 = input("Wybierz opcję: ")

        if wybor2 == "1":
            print("\n📦 TWORZENIE NOWEJ AWIZACJI")

            delivery_date = input("Data dostawy (DD/MM/RRRR): ")
            delivery_type = input("Typ dostawy: ")
            unit_type = input("Typ jednostki: ")


            delivery_id = sum(1 for _ in open("archive/pre-advice.csv", encoding='utf-8')) if os.path.exists("archive/pre-advice.csv") else 0

            delivery = Delivery(
                id=delivery_id,
                login=login,
                company=company,

                delivery_date=delivery_date,
                delivery_type=delivery_type,
                unit_type=unit_type,

            )

            delivery.save_to_file("archive/pre-advice.csv")
            print("✅ Awizacja została zapisana!")



        elif wybor2 == "2":

            path = "archive/pre-advice.csv"

            if not os.path.exists(path):
                print("📭 Brak zapisanych awizacji.")

                continue

            with open(path, encoding="utf-8", newline="") as f:

                r = csv.reader(f, delimiter=";")

                try:

                    header = next(r)  # pierwszy wiersz jako nagłówek

                except StopIteration:

                    print("📭 Plik jest pusty.")

                    continue

                matches = []

                for row in r:

                    if len(row) > 1 and row[1].strip() == login:  # szukaj TYLKO po 2. kolumnie

                        matches.append([c.strip() for c in row])

            if matches:

                print("\n🗂️ Twoje awizacje:")

                print(" | ".join(h.strip() for h in header))  # nagłówki

                for row in matches:  # dopasowane wiersze (łącznie z ID)

                    print(" | ".join(row))
                    break

            else:

                print("📭 Brak awizacji dla tego użytkownika.")



        elif wybor2 == "3":
            print("👋 Wylogowano.")
            break

        else:
            print("⚠️ Nieprawidłowa opcja.")
