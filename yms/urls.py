# yms/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("awizacje.urls")),                 # strona główna + widoki aplikacji
    path("accounts/", include("django.contrib.auth.urls")),  # ⬅️ DODAĆ to
    path("admin/", admin.site.urls),
]
