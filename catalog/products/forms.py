from django import forms
from models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["contact_name", "contact_email", "contact_phone", "address"]
        labels = {
            "contact_name": "Your Name",
            "contact_email": "Your Email",
            "contact_phone": "Your Phone",
            "address": "Your Address",
        }
