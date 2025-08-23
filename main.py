
import os
import csv

from core.user_manager import UserManager # <- twoja klasa z pliku users.py
from core.delivery import Delivery # <- twoja klasa Delivery
from menus.user_menu import run_user_menu        # <- funkcja z menus.py

# --- INICJALIZACJA PRZED UŻYCIEM ---
um = UserManager(r"C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\users.csv")
um.load_users()
# -----------------------------------

while True:
    print("\n📋 MENU GŁÓWNE")
    print("1. 🔐 Zaloguj się")
    print("2. 📝 Zarejestruj się")
    print("3. ❌ Wyjście")
    wybor = input("Wybierz opcję (1/2/3): ").strip()

    if wybor == "1":
        login = input("Login: ").strip()
        haslo = input("Hasło: ")
        if um.authenticate(login, haslo):
            print(f"✅ Zalogowano pomyślnie! Witaj, {login}")
            company = um.users[login]['kontrahent']
            run_user_menu(login, company, Delivery)
        else:
            print("❌ Niepoprawny login lub hasło.")

    elif wybor == "2":
        login = input("Nowy login: ").strip()
        haslo = input("Hasło: ")
        kontrahent = input("Kontrahent: ").strip()
        um.register_user(login, haslo, kontrahent)
        print("✅ Rejestracja zakończona pomyślnie!")
        break
    elif wybor == "3":
        print('👋 Wylogowano, do zobaczenia!')
        break

    else:
        print("⚠️ Nieprawidłowa opcja. Spróbuj ponownie.")
