from django.urls import path
from . import views

app_name = "awizacje"

urlpatterns = [
    path("", views.home, name="home"),
    path("list/", views.PreadviceListView.as_view(), name="list"),
    path("add/", views.PreadviceCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.PreadviceUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PreadviceDeleteView.as_view(), name="delete"),

    path("login/", views.SignInView.as_view(), name="login"),
    path("logout/", views.signout_get, name="logout"),   # GET logout (bez CSRF)
    path("signup/", views.signup, name="signup"),
]
