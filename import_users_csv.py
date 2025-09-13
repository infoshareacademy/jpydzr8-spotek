# import_users_csv.py  (VERSION v3 for "login;password;company")
import os
import csv
from db.users_repo import create_user_from_plain_password
from db.connection import get_cursor  # do opcjonalnej aktualizacji hasła

CSV_PATH = r"C:\Users\tomas\PycharmProjects\jpydzr8-spotek\db\users.csv"
DEFAULT_PASSWORD = "Start123!"          # użyte gdy pole password jest puste
UPDATE_EXISTING_PASSWORD = False        # ustaw True, aby nadpisywać hasła istniejącym użytkownikom

print("VERSION v3")

def user_exists(login: str) -> bool:
    sql = "SELECT 1 FROM users WHERE login=%s LIMIT 1"
    with get_cursor() as cur:
        cur.execute(sql, (login,))
        return cur.fetchone() is not None

def update_password(login: str, plain_password: str) -> None:
    # bezpieczne: zmień hasło tylko gdy prosimy (UPDATE_EXISTING_PASSWORD=True)
    from db.users_repo import create_user_from_plain_password  # użyjemy tej samej logiki hashowania
    # sztuczka: wstaw tymczasowego usera żeby dostać hash? Nie, zrobimy UPDATE przez własny hash:
    import bcrypt
    password_hash = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    sql = "UPDATE users SET password_hash=%s WHERE login=%s"
    with get_cursor(commit=True) as cur:
        cur.execute(sql, (password_hash, login))

def import_users():
    if not os.path.exists(CSV_PATH):
        print(f"❌ Nie znaleziono pliku: {CSV_PATH}")
        return

    added = 0
    updated = 0
    skipped = 0

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        headers = [h.strip().lower() for h in (reader.fieldnames or [])]
        print(f"DEBUG: headers={headers}")

        required = {"login", "password", "company"}
        if not required.issubset(set(headers)):
            print("❌ CSV musi mieć nagłówki: login;password;company (w tej kolejności lub dowolnej).")
            return

        for i, row in enumerate(reader, start=2):
            login = (row.get("login") or row.get("LOGIN") or "").strip()
            password = (row.get("password") or row.get("PASSWORD") or "").strip()
            # company jest tu ignorowane (możesz kiedyś dodać kolumnę w users)
            if not login:
                print(f"⚠️ Linia {i}: brak loginu – pomijam.")
                skipped += 1
                continue

            plain = password if password else DEFAULT_PASSWORD

            try:
                if user_exists(login):
                    if UPDATE_EXISTING_PASSWORD:
                        update_password(login, plain)
                        print(f"🔁 Zaktualizowano hasło: {login}")
                        updated += 1
                    else:
                        print(f"➡️  Istnieje: {login} – pomijam (nie aktualizuję haseł).")
                        skipped += 1
                else:
                    create_user_from_plain_password(login, plain)
                    print(f"✅ Dodano: {login}")
                    added += 1
            except Exception as e:
                print(f"❌ Linia {i}: błąd dla '{login}': {e}")
                skipped += 1

    print(f"✔️ Gotowe. Dodano: {added}, Zaktualizowano: {updated}, Pomięto: {skipped}")

if __name__ == "__main__":
    import_users()
