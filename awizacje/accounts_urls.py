from django.urls import path
from .views_auth import register  # <-- import z oddzielnego modułu

urlpatterns = [
    path("register/", register, name="register"),
]
