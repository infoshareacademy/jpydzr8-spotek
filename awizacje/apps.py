from __future__ import annotations
from django.apps import AppConfig

class AwizacjeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "awizacje"

    def ready(self) -> None:
        # Brak importów modelu Delivery — już nie istnieje.
        # Jeśli kiedyś będą sygnały:
        # from . import signals  # noqa: F401
        pass
