# dbcore/models.py
from __future__ import annotations

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class DeliveryType(models.Model):
    Delivery_type = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("Delivery_type",)

    def __str__(self) -> str:
        return self.Delivery_type


class HUType(models.Model):
    HU_type = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("HU_type",)

    def __str__(self) -> str:
        return self.HU_type


class PreAdvice(models.Model):
    # mapowanie na kolumnę delivery_date
    date = models.DateField(db_column="delivery_date")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="preadvices")
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.PROTECT, related_name="preadvices")

    login = models.CharField(max_length=150, db_index=True)

    driver_name = models.CharField(max_length=255, null=True, blank=True)
    driver_phone = models.CharField(max_length=50, null=True, blank=True)
    driver_lang = models.CharField(max_length=10, null=True, blank=True)
    vehicle_number = models.CharField(max_length=50, null=True, blank=True)
    trailer_number = models.CharField(max_length=50, null=True, blank=True)
    order_number = models.CharField(max_length=100, null=True, blank=True)

    # pola „załącznikowe” z bazy — luźne, żeby INSERT nie wywalał się o brak domyślnych
    attachment_name = models.CharField(max_length=255, null=True, blank=True, default="", db_column="attachment_name")
    attachment_size_bytes = models.BigIntegerField(null=True, blank=True, db_column="attachment_size_bytes")
    attachment_path = models.CharField(max_length=500, null=True, blank=True, default="", db_column="attachment_path")

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self) -> str:
        return f"[{self.id}] {self.date} / {self.company.name}"

    @property
    def hu_summary(self) -> str:
        rows = self.hu_rows.select_related("hu_type").all()
        if not rows:
            return "-"
        return ", ".join(f"{r.hu_type.HU_type}={r.quantity}" for r in rows)


class PreAdviceHU(models.Model):
    preadvice = models.ForeignKey(
        PreAdvice,
        on_delete=models.CASCADE,
        related_name="hu_rows",
    )
    hu_type = models.ForeignKey(HUType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("preadvice", "hu_type")

    def __str__(self) -> str:
        return f"{self.preadvice_id} / {self.hu_type.HU_type} = {self.quantity}"
