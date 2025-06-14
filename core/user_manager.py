# Klasa odpowiedzialna za zarządzanie użytkownikami.
# - ładuje użytkowników z pliku CSV
# - przechowuje ich w słowniku (login jako klucz)
# - pozwala sprawdzić, czy dane logowania są poprawne
import csv


class UserManager:

    def __init__(self, sciezka_do_pliku):# Konstruktor klasy
         self.sciezka = sciezka_do_pliku # Zapamiętuje ścieżkę do pliku
         self.users = {} # Tworzy pusty słownik na użytkowników

    def load_users(self):
        with open(self.sciezka, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                self.users[row['login']] = {
                    'haslo': row['password'],
                    'kontrahent': row['company']
                }

    def authenticate(self, login, haslo):
        if login in self.users:
            if self.users[login]['haslo'] == haslo:
                return True
        return False


    def register_user(self, login, haslo, kontrahent):
        if login in self.users:
            print("❌ Użytkownik już istnieje.")
            return

    # Zapis do pliku CSV
        with open(self.sciezka, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([login, haslo, kontrahent])

    # Dodanie do pamięci (słownika)
        self.users[login] = {
            'haslo': haslo,
            'kontrahent': kontrahent
        }
        print("✅ Użytkownik został zarejestrowany.")
