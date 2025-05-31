from core.auth import authenticate, load_users_from_csv
from dashboard.menu import main_menu
from deliveries.create import create_awizacja

def run():
    users = load_users_from_csv()
    email = input("Email: ")
    haslo = input("Hasło: ")
    role = authenticate(email, haslo, users)
    if not role:
        print("❌ Nieprawidłowe dane logowania")
        return

    while True:
        opcja = main_menu(role)
        if opcja == "1":
            create_awizacja()
        elif opcja == "2":
            break
        else:
            print("❌ Nieprawidłowa opcja")

if __name__ == "__main__":
    run()
