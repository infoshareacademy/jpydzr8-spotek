def main_menu(role):
    print("\n=== PANEL AWIZACJI ===")
    if role == "operator":
        print("1. Załóż awizację")
        print("2. Wyjście")
        choice = input("Wybierz opcję: ")
        return choice
