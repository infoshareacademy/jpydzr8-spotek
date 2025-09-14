from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserManager:
    """
    Obsługa użytkowników na bazie Django auth_user.
    """

    def register_user(self, username: str, password: str, company: str = None) -> bool:
        """
        Rejestracja nowego użytkownika (zwykły user).
        Firma jest ignorowana, bo auth_user jej nie przechowuje.
        """
        if User.objects.filter(username=username).exists():
            print(f"⚠ Użytkownik {username} już istnieje.")
            return False
        User.objects.create_user(username=username, password=password)
        print(f"✅ Użytkownik {username} został zarejestrowany.")
        return True

    def authenticate(self, username: str, password: str) -> bool:

        """
        Sprawdza dane logowania.
        """
        user = authenticate(username=username, password=password)
        if user is not None:

            return True
        else:
            print(f"❌ Błędne dane logowania dla {username}.")
            return False

    def list_users(self):
        """
        Lista wszystkich użytkowników.
        """
        return list(User.objects.values_list("id", "username"))
