from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail


def send_confirmation_mail(request, user, email, confirm_view: str):
    confirm_url = request.build_absolute_uri(reverse(f"accounts:{confirm_view}"))
    confirm_url += f"?user={user.id}&email={email}"
    subject = "Confirm new email"
    message = f"Hello, {user.username} you want to confirm your email? Confirm your email on link: {confirm_url}"
    send_mail(subject, message, "no-reply", [email], fail_silently=False)
    messages.info(request, "Confirmation email was send")
