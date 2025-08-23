import csv

class UserManager:
    def __init__(self, sciezka_do_pliku):
        self.sciezka = sciezka_do_pliku
        self.users = {}  # pusty słownik

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

    def register_user(self, login: object, haslo: object, kontrahent: object) -> None:
        if login in self.users:
            print("❌ Użytkownik już istnieje.")
            return  # <-- to musi być w tym samym bloku co print

        with open(self.sciezka, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([login, haslo, kontrahent])

        self.users[login] = {
            'haslo': haslo,
            'kontrahent': kontrahent
        }
        print("✅ Użytkownik został zarejestrowany.")
