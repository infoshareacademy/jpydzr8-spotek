# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    """
    Prosta rejestracja użytkownika z wbudowanym UserCreationForm.
    Po sukcesie przekierowuje na ekran logowania.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało utworzone. Możesz się zalogować.")
            return redirect("login")
        messages.error(request, "Popraw błędy w formularzu.")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form, "title": "Rejestracja"})
