from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=290)
    slug = models.SlugField(unique=True)
    profile = models.ImageField(upload_to="products/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        total = 0
        for cart_item in self.cart_items.all():
            total = total + cart_item.total()
        return total

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_item", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return self.quantity * self.product.price
        

class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        total_price = 0
        for item in self.order_items.all():
            total_price += item.total()
        return total_price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_item", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="order_items", on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return self.quantity * self.product.price        