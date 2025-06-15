from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.place_order, name='place_order'),
    path('status/<int:order_id>/', views.order_status, name='order_status'),
    path('confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
]