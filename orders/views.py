from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Order
from .forms import OrderForm
from django.conf import settings

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'Order Placed'
            order.save()

            # Send email to warehouse
            subject = f'New Order #{order.id}'
            context = {
                'order': order,
                'confirmation_link': f'http://localhost:8000/confirm/{order.id}/'
            }
            html_message = render_to_string('orders/warehouse_email.html', context)
            send_mail(
                subject,
                '',
                settings.EMAIL_HOST_USER,
                ['warehouseemail2025@gmail.com'],
                html_message=html_message
            )
            return redirect('orders:order_status', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_status.html', {'order': order})

def confirm_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Pending Confirmation'
    order.save()
    return render(request, 'orders/confirmation.html', {'order': order})