# db/deliveries_repo.py
from db.connection import get_cursor

# Dozwolone wartości zgodne z ENUM w tabeli MySQL
ALLOWED_DELIVERY_TYPES = {"paczka", "luz", "kontener", "palety"}
ALLOWED_UNIT_TYPES = {"HU", "karton", "paleta"}

def add_delivery(login: str, supplier: str, delivery_date: str, delivery_type: str, unit_type: str, notes: str | None = None) -> int:
    """
    Zapisuje rekord do tabeli deliveries i zwraca ID nowego rekordu.
    delivery_date w formacie 'YYYY-MM-DD'
    """
    # Walidacja zgodna z ENUM w MySQL
    if delivery_type not in ALLOWED_DELIVERY_TYPES:
        raise ValueError(f"delivery_type musi być jednym z: {sorted(ALLOWED_DELIVERY_TYPES)}")
    if unit_type not in ALLOWED_UNIT_TYPES:
        raise ValueError(f"unit_type musi być jednym z: {sorted(ALLOWED_UNIT_TYPES)}")

    sql = """
        INSERT INTO deliveries (login, supplier, delivery_date, delivery_type, unit_type, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (login, supplier, delivery_date, delivery_type, unit_type, notes)

    with get_cursor(commit=True) as cur:
        cur.execute(sql, values)
        return cur.lastrowid

def get_deliveries_for_login(login: str, limit: int = 100):
    """
    Pobiera ostatnie rekordy z deliveries dla danego loginu.
    """
    sql = """
        SELECT id, login, supplier, delivery_date, delivery_type, unit_type, notes, created_at
        FROM deliveries
        WHERE login = %s
        ORDER BY id DESC
        LIMIT %s
    """
    with get_cursor() as cur:
        cur.execute(sql, (login, limit))
        return cur.fetchall()
