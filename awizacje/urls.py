from django.urls import path
from . import views

app_name = "awizacje"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("add/", views.add_view, name="add"),
    path("<int:pk>/edit/", views.edit_view, name="edit"),
    path("<int:pk>/delete/", views.soft_delete_view, name="delete"),
]
