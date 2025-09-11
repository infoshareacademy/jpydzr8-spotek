from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

DELIVERY_TYPES = [
    ("Dostawa paczka",   "Dostawa paczka"),
    ("Dostawa luz",      "Dostawa luz"),
    ("Dostawa kontener", "Dostawa kontener"),
    ("Dostawa palety",   "Dostawa palety"),
]

def validate_filesize_10mb(f):
    if f and f.size > 10 * 1024 * 1024:
        raise ValidationError("Załącznik przekracza 10 MB.")

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deliveries")
    company = models.CharField("Firma", max_length=120, blank=True)

    delivery_date = models.DateField("Data dostawy")
    delivery_type = models.CharField("Typ dostawy", max_length=32, choices=DELIVERY_TYPES)

    # HU – trzy ilości (ułamki dozwolone, >= 0)
    hu_paleta   = models.DecimalField("Paleta",   max_digits=18, decimal_places=3, default=0)
    hu_karton   = models.DecimalField("Karton",   max_digits=18, decimal_places=3, default=0)
    hu_kontener = models.DecimalField("Kontener", max_digits=18, decimal_places=3, default=0)

    # Dane kierowcy (opcjonalne)
    driver_name  = models.CharField("Imię i nazwisko kierowcy", max_length=120, blank=True)
    driver_phone = models.CharField("Telefon kierowcy", max_length=32, blank=True)
    truck_no     = models.CharField("Nr auta (ciągnik)", max_length=32, blank=True)
    trailer_no   = models.CharField("Nr naczepy", max_length=32, blank=True)

    # Zamówienie (opcjonalne)
    order_no = models.CharField("Numer zamówienia", max_length=64, blank=True)

    # Załącznik (≤ 10 MB)
    attachment = models.FileField(
        "Załącznik",
        upload_to="attachments/%Y/%m/",
        validators=[validate_filesize_10mb],
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # soft-delete

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.delivery_type} {self.delivery_date:%d.%m.%Y}"

    def soft_delete_and_scrub(self):
        """Czyści dane, ale zostawia ID/user/created_at; ustawia deleted_at."""
        from django.utils import timezone
        self.delivery_type = "(usunięta)"
        self.hu_paleta = self.hu_karton = self.hu_kontener = 0
        self.driver_name = self.driver_phone = ""
        self.truck_no = self.trailer_no = ""
        self.order_no = ""
        if self.attachment:
            self.attachment.delete(save=False)
            self.attachment = None
        self.deleted_at = timezone.now()
        self.save()
