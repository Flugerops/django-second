from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string


from accounts.forms import RegisterForm, ProfileUpdateForm, RegisterFormNoCaptcha
from accounts.models import Profile
from products.models import Cart, Product, CartItem, Order, OrderItem


def send_confirmation_mail(request, user, email, confirm_view: str):
    confirm_url = request.build_absolute_uri(reverse(f"accounts:{confirm_view}"))
    confirm_url += f"?user={user.id}&email={email}"
    subject = "Confirm new email"
    message = f"Hello, {user.username} you want to confirm your email? Confirm your email on link: {confirm_url}"
    send_mail(subject, message, "no-reply", [email], fail_silently=False)
    messages.info(request, "Confirmation email was send")


def send_order_confirmation_email(order: Order):
    subject = f"Order Confirmation for Order № {Order.id}"
    context = {"order": order}
    text_content = render_to_string(
        "catalog/templates/email/order_confirmation_email.txt", context
    )
    to_email = order.contact_email

    try:
        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [to_email, settings.ADMIN_EMAIL],
        )

    except Exception as e:
        print(f"Error sending mail: {e}")
