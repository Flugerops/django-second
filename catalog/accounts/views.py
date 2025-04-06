from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products:index")
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url or "products:home")
        else:
            return render(
                request, "login.html", context={"error": "Incorrect login or password"}
            )
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("products:index")


@login_required
def profile(request):
    return render(request, "profile.html")
