# menus/user_menu.py
from .pre_advice_create import (
    create_pre_advice_quick_cli,
    ensure_archive_and_header,
    ARCHIVE_PATH,
    ATTACH_DIR,
    MAX_ATTACH_BYTES,
)
from .pre_advice_manage import handle_my_advices_menu

def run_user_menu(login, company, Delivery):
    while True:
        print("\n🧾 MENU UŻYTKOWNIKA")
        print("1. ➕ Dodaj awizację")
        print("2. 📄 Moje awizacje (lista/edycja/usuwanie)")
        print("3. 🔙 Wyloguj")
        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            create_pre_advice_quick_cli(login, company, Delivery)
        elif wybor == "2":
            ensure_archive_and_header()
            handle_my_advices_menu(
                login=login,
                path=ARCHIVE_PATH,
                attach_dir=ATTACH_DIR,
                max_attach_bytes=MAX_ATTACH_BYTES,
            )
        elif wybor == "3":
            print("👋 Wylogowano.")
            break
        else:
            print("⚠️ Nieprawidłowa opcja.")
