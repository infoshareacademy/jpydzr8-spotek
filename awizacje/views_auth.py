from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    """
    Prosta rejestracja użytkownika na bazie wbudowanego UserCreationForm.
    Po udanej rejestracji loguje usera i wraca na stronę startową.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # nazwa widoku strony startowej
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
