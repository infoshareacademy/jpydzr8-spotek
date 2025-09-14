from __future__ import annotations

from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dbcore.models import PreAdvice, PreAdviceHU
from .forms import PreAdviceForm, FilterForm, SignupForm


def home(request: HttpRequest) -> HttpResponse:
    """
    Strona startowa:
    - gość: 'Zaloguj się' / 'Rejestracja'
    - zalogowany: skróty do listy/dodawania/wylogowania
    """
    return render(request, "home.html")


class SignInView(LoginView):
    template_name = "registration/login.html"
    next_page = reverse_lazy("awizacje:home")


@login_required
def signout_get(request: HttpRequest) -> HttpResponse:
    """
    BEZ CSRF: wylogowanie po GET.
    Zabezpieczone login_required (wymaga bycia zalogowanym).
    """
    logout(request)
    return redirect("awizacje:login")


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Konto utworzone i zalogowano.")
            return redirect("awizacje:home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


class PreadviceListView(LoginRequiredMixin, ListView):
    model = PreAdvice
    template_name = "preadvice_list.html"
    context_object_name = "items"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            PreAdvice.objects.select_related("company", "delivery_type")
            .prefetch_related("hu_rows__hu_type")
            .order_by("-date", "-id")
        )
        if not self.request.user.is_superuser:
            qs = qs.filter(login=self.request.user.username)

        form = FilterForm(self.request.GET or None)
        if form.is_valid():
            dfrom = form.cleaned_data.get("date_from")
            dto = form.cleaned_data.get("date_to")
            comp = form.cleaned_data.get("company")
            dtyp = form.cleaned_data.get("delivery_type")
            if dfrom:
                qs = qs.filter(date__gte=dfrom)
            if dto:
                qs = qs.filter(date__lte=dto)
            if comp:
                qs = qs.filter(company=comp)
            if dtyp:
                qs = qs.filter(delivery_type=dtyp)
        self.filter_form = form
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = getattr(self, "filter_form", FilterForm())
        return ctx


HUFormSet = inlineformset_factory(
    PreAdvice,
    PreAdviceHU,
    fields=("hu_type", "quantity"),
    extra=1,
    can_delete=True,
)


class PreadviceCreateView(LoginRequiredMixin, CreateView):
    model = PreAdvice
    form_class = PreAdviceForm
    template_name = "preadvice_form.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = HUFormSet(self.request.POST)
        else:
            ctx["formset"] = HUFormSet()
        return ctx

    def form_valid(self, form: PreAdviceForm) -> HttpResponse:
        form.instance.login = self.request.user.username
        response = super().form_valid(form)
        formset = HUFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, "Awizacja dodana.")
            return redirect("awizacje:list")
        self.object.delete()
        return self.form_invalid(form)

    def get_success_url(self) -> str:
        return reverse("awizacje:list")


class PreadviceUpdateView(LoginRequiredMixin, UpdateView):
    model = PreAdvice
    form_class = PreAdviceForm
    template_name = "preadvice_form.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(login=self.request.user.username)
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = HUFormSet(self.request.POST, instance=self.object)
        else:
            ctx["formset"] = HUFormSet(instance=self.object)
        return ctx

    def form_valid(self, form: PreAdviceForm) -> HttpResponse:
        response = super().form_valid(form)
        formset = HUFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, "Awizacja zaktualizowana.")
            return redirect("awizacje:list")
        return self.form_invalid(form)

    def get_success_url(self) -> str:
        return reverse("awizacje:list")


class PreadviceDeleteView(LoginRequiredMixin, DeleteView):
    model = PreAdvice
    template_name = "preadvice_confirm_delete.html"
    success_url = reverse_lazy("awizacje:list")

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(login=self.request.user.username)
        return qs
