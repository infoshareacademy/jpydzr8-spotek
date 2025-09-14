from __future__ import annotations
import os


def _ensure_django() -> None:
    """Inicjalizacja Django, aby ORM działał także poza manage.py."""
    try:
        from django.conf import settings  # type: ignore
        if settings.configured:
            return
    except Exception:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yms.settings")
    import django  # type: ignore
    django.setup()


if __name__ == "__main__":
    _ensure_django()
    from core.user_menu import start_menu
    start_menu()

