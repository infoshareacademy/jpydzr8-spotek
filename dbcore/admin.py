# dbcore/admin.py
from django.contrib import admin
from .models import Company, DeliveryType, HUType, PreAdvice, PreAdviceHU


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "Delivery_type")
    search_fields = ("Delivery_type",)
    ordering = ("Delivery_type",)


@admin.register(HUType)
class HUTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "HU_type")
    search_fields = ("HU_type",)
    ordering = ("HU_type",)


class PreAdviceHUInline(admin.TabularInline):
    model = PreAdviceHU
    extra = 0
    autocomplete_fields = ("hu_type",)
    fields = ("hu_type", "quantity")


@admin.register(PreAdvice)
class PreAdviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "company",
        "delivery_type",
        "login",
        "driver_name",
        "vehicle_number",
        "trailer_number",
        "order_number",
    )
    list_filter = ("company", "delivery_type", "date")
    search_fields = ("login", "driver_name", "driver_phone", "vehicle_number", "trailer_number", "order_number")
    autocomplete_fields = ("company", "delivery_type")
    inlines = [PreAdviceHUInline]
    ordering = ("-date", "-id")
