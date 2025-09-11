from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Delivery
from .forms import DeliveryForm, DeliveryEditForm

@login_required
def list_view(request):
    # superuser widzi wszystko, zwykły user tylko swoje
    if request.user.is_superuser:
        rows = Delivery.objects.all().order_by("-created_at")
    else:
        rows = Delivery.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "awizacje/list.html", {"rows": rows})

@login_required
def add_view(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            d: Delivery = form.save(commit=False)
            d.user = request.user
            d.save()
            messages.success(request, "Awizacja zapisana.")
            return redirect("awizacje:list")
        messages.error(request, "Popraw błędy w formularzu.")
    else:
        form = DeliveryForm()
    return render(request, "awizacje/form.html", {"form": form, "title": "Dodaj awizację"})

@login_required
def edit_view(request, pk: int):
    d = get_object_or_404(Delivery, pk=pk)
    # tylko właściciel lub superuser
    if not (request.user.is_superuser or d.user_id == request.user.id):
        messages.error(request, "Brak uprawnień do edycji tej awizacji.")
        return redirect("awizacje:list")

    if request.method == "POST":
        form = DeliveryEditForm(request.POST, request.FILES, instance=d)
        if form.is_valid():
            if form.cleaned_data.get("remove_attachment") and d.attachment:
                d.attachment.delete(save=False)
                d.attachment = None
            form.save()
            messages.success(request, "Zapisano zmiany.")
            return redirect("awizacje:list")
        messages.error(request, "Popraw błędy w formularzu.")
    else:
        form = DeliveryEditForm(instance=d)
    return render(request, "awizacje/form.html", {"form": form, "title": f"Edytuj awizację #{d.pk}"})

@login_required
def soft_delete_view(request, pk: int):
    d = get_object_or_404(Delivery, pk=pk)
    # tylko właściciel lub superuser
    if not (request.user.is_superuser or d.user_id == request.user.id):
        messages.error(request, "Brak uprawnień do usunięcia tej awizacji.")
        return redirect("awizacje:list")

    if request.method == "POST":
        d.soft_delete_and_scrub()
        messages.success(request, "Dane awizacji usunięte (ID pozostaje).")
        return redirect("awizacje:list")
    return render(request, "awizacje/confirm_delete.html", {"obj": d})
