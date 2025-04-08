from django.urls import path
from . import views

urlpatterns = [
    path("", views.check_email, name="check_email"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("home/", views.home, name="home"),
    path("restaurant/<int:restaurant_id>/", views.restaurant_menu, name="restaurant_menu"),
    path("add_to_cart/<int:menuitem_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_cart/<int:cartitem_id>/", views.update_cart, name="update_cart"),
    path("order-confirmed/<int:order_id>/", views.order_confirmed, name="order_confirmed"),
    path("order_delivered/<int:order_id>/", views.order_delivered, name="order_delivered"),
]
