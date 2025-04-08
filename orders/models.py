from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

# Restaurant Model
class Restaurant(models.Model):
    restaurant_id = models.BigAutoField(primary_key=True)
    res_name = models.CharField(max_length=255)
    res_email = models.EmailField(unique=True)
    res_phone_number = models.CharField(max_length=15)
    res_address = models.TextField()

    def __str__(self):
        return self.res_name

# Menu Item Model
class MenuItem(models.Model):
    menuitem_id = models.BigAutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()

    def __str__(self):
        return self.item_name

# Cart Model
class Cart(models.Model):
    cart_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

# Cart Item Model
class CartItem(models.Model):
    cartitem_id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name} in Cart"

# Order Model
class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.TextField(default="Not Provided")
    status = models.CharField(max_length=20, default="Order Confirmed")

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

# Order Item Model
class OrderItem(models.Model):
    orderitem_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name} in Order {self.order.order_id}"

# Delivery Personnel Model
class DeliveryPersonnel(models.Model):
    deliverypersonnel_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=[("free", "Free"), ("busy", "Busy")], default="free")

    def __str__(self):
        return f"{self.name} - {self.status}"

# Delivery Model
class Delivery(models.Model):
    delivery_id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPersonnel, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=[
        ('Assigned', 'Assigned'),
        ('On the Way', 'On the Way'),
        ('Delivered', 'Delivered')
    ], default='Assigned')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Order {self.order.order_id} - {self.status} (Handled by {self.delivery_person.name if self.delivery_person else 'Unassigned'})"

# Review Model
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField(default=timezone.now)
    invoice_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"Invoice #{self.invoice_id} for Order #{self.order.order_id}"
