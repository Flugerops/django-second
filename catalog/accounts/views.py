from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile
from .utils import send_confirmation_mail


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_confirmation_mail(request, user, user.email, "confirm_registration")
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
            return redirect(next_url or "products:index")
        else:
            return render(
                request, "login.html", context={"error": "Incorrect login or password"}
            )
    return render(request, "login.html")


@login_required
def edit_profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            # user.email = new_email
            # user.save()
            if new_email != user.email:
                send_confirmation_mail(request, user, new_email, "confirm_email")
                # confirm_url = request.build_absolute_uri(
                #     reverse("accounts:confirm_email")
                # )
                # confirm_url += f"?user={user.id}&email={new_email}"
                # subject = "Confirm new email"
                # message = f"Hello, {user.username} you want to confirm your email? Confirm your email on link: {confirm_url}"
                # send_mail(
                #     subject, message, "no-reply", [new_email], fail_silently=False
                # )
                # messages.info(request, "Confirmation email was send")

            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(user=user)
    return render(
        request, "edit_profile.html", context={"form": form, "profile": profile}
    )


def logout_view(request):
    logout(request)
    return redirect("products:index")


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})


def confirm_email(request):
    user_id = request.GET.get("user")
    email = request.GET.get("email")

    if not user_id or not email:
        return HttpResponseBadRequest("BAD REQUEST: No user or email")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("BAD REQUEST: No user or email")

    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("This email already taken")

    user.email = email
    user.save()

    return render(request, "email_change_done.html", {"email": email})


def confirm_registration(request):
    user_id = request.GET.get("user")
    email = request.GET.get("email")

    if not user_id or not email:
        return HttpResponseBadRequest("BAD REQUEST: No user or email")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("BAD REQUEST: No user or email")

    # if User.objects.filter(email=email).exists():
    #     return HttpResponseBadRequest("This email already taken")

    login(request, user)
    return render(request, "email_change_done.html", {"email": email})
