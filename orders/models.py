from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    product = models.CharField(max_length=100)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    user_email = models.EmailField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"