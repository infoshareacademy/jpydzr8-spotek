# db/users_repo.py
import bcrypt
from db.connection import get_cursor

def create_user_from_plain_password(login: str, plain_password: str, role: str = "user") -> int:
    """
    Tworzy użytkownika z hasłem w postaci hasha bcrypt.
    Zwraca ID nowego użytkownika.
    """
    # hash hasła (bcrypt automatycznie dodaje salt)
    password_hash = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    sql = """
        INSERT INTO users (login, password_hash, role)
        VALUES (%s, %s, %s)
    """
    values = (login, password_hash, role)

    with get_cursor(commit=True) as cur:
        cur.execute(sql, values)
        return cur.lastrowid


def verify_login(login: str, plain_password: str) -> bool:
    """
    Sprawdza, czy podany login/hasło są poprawne.
    """
    sql = "SELECT password_hash FROM users WHERE login = %s"
    with get_cursor() as cur:
        cur.execute(sql, (login,))
        row = cur.fetchone()

    if not row:
        return False

    stored_hash = row[0]
    return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))


def get_all_users():
    """
    Pobiera listę wszystkich użytkowników (bez haseł).
    """
    sql = "SELECT id, login, role, created_at FROM users ORDER BY id ASC"
    with get_cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
