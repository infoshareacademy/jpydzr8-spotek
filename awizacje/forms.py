# awizacje/forms.py
from __future__ import annotations

from datetime import date as date_cls
from typing import Any, Dict, Optional

from django import forms
from django.contrib.auth.models import User

from dbcore.models import Company, DeliveryType, PreAdvice


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "Login", "email": "E-mail (opcjonalnie)"}

    def clean_username(self) -> str:
        username = (self.cleaned_data.get("username") or "").strip()
        if not username:
            raise forms.ValidationError("Login jest wymagany.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Taki login już istnieje.")
        return username

    def clean(self) -> Dict[str, Any]:
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Hasła muszą być identyczne.")
        return cleaned

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PreAdviceForm(forms.ModelForm):
    date = forms.DateField(label="Data dostawy", widget=forms.DateInput(attrs={"type": "date"}))
    company = forms.ModelChoiceField(label="Firma", queryset=Company.objects.all(), empty_label="— wybierz firmę —")
    delivery_type = forms.ModelChoiceField(
        label="Typ dostawy", queryset=DeliveryType.objects.all(), empty_label="— wybierz typ dostawy —"
    )

    driver_name = forms.CharField(label="Kierowca (imię i nazwisko)", required=False)
    driver_phone = forms.CharField(label="Telefon kierowcy", required=False)
    driver_lang = forms.CharField(label="Język (np. PL, EN, UA)", required=False, max_length=10)
    vehicle_number = forms.CharField(label="Numer auta", required=False)
    trailer_number = forms.CharField(label="Numer naczepy", required=False)
    order_number = forms.CharField(label="Numer zamówienia", required=False)

    class Meta:
        model = PreAdvice
        exclude = ["login", "attachment_name", "attachment_size_bytes", "attachment_path"]
        widgets = {"driver_lang": forms.TextInput(attrs={"placeholder": "PL / EN / UA / ..."})}

    def clean_date(self) -> date_cls:
        d: date_cls = self.cleaned_data["date"]
        if d.year < 2000:
            raise forms.ValidationError("Data wygląda na nieprawidłową.")
        return d


class FilterForm(forms.Form):
    date_from = forms.DateField(label="Data od", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(label="Data do", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    company = forms.ModelChoiceField(label="Firma", required=False, queryset=Company.objects.all(), empty_label="— wszystkie —")
    delivery_type = forms.ModelChoiceField(
        label="Typ dostawy", required=False, queryset=DeliveryType.objects.all(), empty_label="— wszystkie —"
    )

    def clean(self) -> Dict[str, Any]:
        cleaned = super().clean()
        d_from: Optional[date_cls] = cleaned.get("date_from")
        d_to: Optional[date_cls] = cleaned.get("date_to")
        if d_from and d_to and d_from > d_to:
            self.add_error("date_to", "Data do nie może być wcześniejsza niż data od.")
        return cleaned
