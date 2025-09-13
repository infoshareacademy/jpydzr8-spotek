# seed_users_and_companies.py
from db.users_repo import create_user_from_plain_password, assign_user_to_company

DEFAULT_PASSWORD = "Start123!"

def seed():
    for i in range(1, 11):
        login = f"user_{i}"
        # 1. utwórz usera
        try:
            uid = create_user_from_plain_password(login, DEFAULT_PASSWORD)
            print(f"✅ Utworzono {login} (id={uid})")
        except Exception as e:
            print(f"⚠️ User {login} już istnieje? {e}")

        # 2. przypisz firmę Company_i
        company_name = f"Company_{i}"
        try:
            assign_user_to_company(login, company_name)
            print(f"➡️ {login} przypisany do {company_name}")
        except Exception as e:
            print(f"⚠️ Błąd przypisania {login}→{company_name}: {e}")

    # Dodatkowo: user_1 ma też Company_10
    try:
        assign_user_to_company("user_1", "Company_10")
        print("🔁 user_1 dostał dodatkowo Company_10")
    except Exception as e:
        print(f"⚠️ Błąd przypisania user_1→Company_10: {e}")

if __name__ == "__main__":
    seed()
