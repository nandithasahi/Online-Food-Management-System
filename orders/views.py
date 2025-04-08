from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.db.models import F
from decimal import Decimal
from .models import (
    Restaurant, MenuItem, Cart, CartItem, Order, OrderItem, 
    Delivery, DeliveryPersonnel, Review, Payment
)
import random, string 

def check_email(request):
    """ Check if email exists and redirect accordingly """
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        if User.objects.filter(email=email).exists():
            return redirect("login")
        return redirect("register")
    return render(request, "orders/check_email.html")



def register(request):
    """ User Registration """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Use custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "orders/register.html", {"form": form})


def user_login(request):
    """ User Login """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "orders/login.html", {"form": form})


@login_required
def user_logout(request):
    """ Logout user """
    logout(request)
    return redirect("check_email")


@login_required
def home(request):
    """ Show all restaurants """
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        print(f"ID: {restaurant.restaurant_id}, Name: {restaurant.res_name}")
    return render(request, "orders/home.html", {"restaurants": restaurants})

@login_required
def restaurant_menu(request, restaurant_id):
    """ Display menu items for a selected restaurant """
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, "orders/menu.html", {"restaurant": restaurant, "menu_items": menu_items})

@login_required
def add_to_cart(request, menuitem_id):
    """ Add item to cart, clearing old items if restaurant changes """
    menu_item = get_object_or_404(MenuItem, menuitem_id= menuitem_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if cart_items.exists() and cart_items.first().item.restaurant != menu_item.restaurant:
        cart_items.delete()  
        message = "Cart cleared. Added to cart."
    else:
        message = "Added to cart!"

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=menu_item)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity = F("quantity") + 1  
    cart_item.save()

    return JsonResponse({"success": True, "message": message})


@login_required
def view_cart(request):
    """ Display cart items and total price """
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []
    total_price = sum(item.quantity * item.item.item_price for item in cart_items)

    return render(request, "orders/cart.html", {"cart_items": cart_items, "total_price": total_price})


@login_required
def update_cart(request, cartitem_id):
    """ Update cart item quantity or remove item """
    cart_item = get_object_or_404(CartItem, cartitem_id=cartitem_id, cart__user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity = F("quantity") + 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity = F("quantity") - 1
        elif action == "remove":
            cart_item.delete()
            return redirect("view_cart")

        cart_item.save()
    return redirect("view_cart")


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    subtotal = sum(item.item.item_price * item.quantity for item in cart_items)
    gst = subtotal * Decimal("0.18")
    delivery_charge = Decimal("10.00")
    total_price = subtotal + gst + delivery_charge

    if request.method == "POST":
        delivery_address = request.POST.get("delivery_address")
        payment_mode = request.POST.get("payment_mode")
        amount = request.POST.get("amount")

        if not delivery_address or not payment_mode or not amount:
            messages.error(request, "All payment fields are required.")
            return redirect("checkout")

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            delivery_address=delivery_address,
            status="Pending"
        )

        # Create order items
        OrderItem.objects.bulk_create([
            OrderItem(order=order, item=item.item, quantity=item.quantity, price=item.item.item_price)
            for item in cart_items
        ])

        # Assign delivery personnel
        delivery_person = DeliveryPersonnel.objects.filter(status="free").first()
        if delivery_person:
            Delivery.objects.create(order=order, delivery_person=delivery_person, status="Assigned")
            delivery_person.status = "busy"
            delivery_person.save()
            messages.success(request, f"Order placed! Delivery assigned to {delivery_person.name}.")
        else:
            messages.warning(request, "No free delivery personnel available at the moment.")

        # Generate and save payment
        invoice_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        Payment.objects.create(
            order=order,
            user=request.user,
            amount=Decimal(amount),
            payment_mode=payment_mode,
            invoice_id=invoice_id
        )

        # Clear cart
        cart_items.delete()

        # Redirect to order confirmed
        return redirect(reverse("order_confirmed", args=[order.order_id]))

    return render(request, "orders/checkout.html", {
        "subtotal": subtotal,
        "gst": gst,
        "delivery_charge": delivery_charge,
        "total_price": total_price
    })

@login_required
def order_confirmed(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    delivery = Delivery.objects.filter(order=order).first()

    if not delivery:
        free_person = DeliveryPersonnel.objects.filter(status="free").first()
        if free_person:
            delivery = Delivery.objects.create(order=order, delivery_person=free_person)
            free_person.status = "busy"
            free_person.save()

    return render(request, "orders/order_confirmed.html", {
        "order": order,
        "order_items": order_items,
        "delivery": delivery
    })

@login_required
def order_delivered(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    delivery = get_object_or_404(Delivery, order=order)
    review_submitted = Review.objects.filter(order=order, user=request.user).exists()

    if request.method == "POST":
        # Handle "Mark as Delivered"
        if "mark_delivered" in request.POST:
            delivery.status = "Delivered"
            delivery.save()

        # Handle Review Submission
        elif "review_text" in request.POST and not review_submitted:
            review_text = request.POST.get("review_text")
            if review_text:
                Review.objects.create(order=order, user=request.user, description=review_text)
                review_submitted = True

    return render(request, "orders/order_delivered.html", {
        "order": order,
        "delivery": delivery,
        "review_submitted": review_submitted
    })
