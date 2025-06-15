from django import forms
from .models import Order

PRODUCT_FORMATS = [
    ('Laptop', 'Laptop'),
    ('Smartphone', 'Smartphone'),
    ('Tablet', 'Tablet'),
    ('Headphones', 'Headphones'),
]

class OrderForm(forms.ModelForm):
    product = forms.ChoiceField(choices=PRODUCT_FORMATS)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_id', 'quantity', 'product', 'product_cost', 'user_email']