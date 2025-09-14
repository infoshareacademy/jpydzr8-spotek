from __future__ import annotations

"""
Ta aplikacja webowa używa modelu PreAdvice z appki 'dbcore'
jako jedynego źródła prawdy (tabela: dbcore_preadvice).

Dodatkowo udostępniamy funkcję validate_filesize_10mb, ponieważ
stare migracje 'awizacje' importują ją z awizacje.models.
To jest tylko kompatybilność wsteczna dla migracji.
"""

from django.core.exceptions import ValidationError

# ---- Backward-compat dla starych migracji awizacje ----
def validate_filesize_10mb(file_obj) -> None:
    """
    Walidator używany w historycznych migracjach (nie w bieżącym modelu).
    Podnosi ValidationError > 10 MB.
    """
    max_bytes = 10 * 1024 * 1024  # 10 MB, tak jak w starej migracji
    size = getattr(file_obj, "size", None)
    if size is None:
        return
    if int(size) > max_bytes:
        raise ValidationError("Plik jest większy niż 10 MB (limit historycznej migracji).")


# ---- Re-export aktualnego modelu z dbcore ----
from dbcore.models import PreAdvice  # noqa: E402,F401

__all__ = ["PreAdvice", "validate_filesize_10mb"]
