# menus/my_deliveries_db.py
from db.deliveries_repo import get_deliveries_for_login

def list_my_deliveries_db(login: str, limit: int = 20):
    """
    Prosty listing ostatnich awizacji z MySQL dla zalogowanego użytkownika.
    """
    rows = get_deliveries_for_login(login=login, limit=limit)

    if not rows:
        print("🟨 Brak danych w bazie dla Twojego loginu.")
        return

    print("\n📄 Ostatnie awizacje (DB):")
    print("-" * 100)
    print(f"{'ID':<5} {'Login':<12} {'Supplier':<18} {'Data':<12} {'Typ':<10} {'Unit':<8} {'Utworzono'}")
    print("-" * 100)
    for (id_, login_, supplier, delivery_date, delivery_type, unit_type, notes, created_at) in rows:
        print(f"{id_:<5} {login_:<12} {supplier:<18} {str(delivery_date):<12} {delivery_type:<10} {unit_type:<8} {str(created_at)}")
    print("-" * 100)
