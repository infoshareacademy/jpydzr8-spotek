
from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id","user","delivery_date","delivery_type","created_at","deleted_at")
    list_filter = ("delivery_type","created_at","deleted_at")
    search_fields = ("id","user__username","order_no","driver_name","truck_no","trailer_no")
