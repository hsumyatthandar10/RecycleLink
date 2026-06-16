from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import render, redirect, get_object_or_404
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="ccategories", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        # Check if `category` is not None before trying to access its name
        if self.category:
            return f"{self.name} (under {self.category.name})"
        else:
            return self.name # Display only the subcategory name if no category is set


class Brand(models.Model):
    name = models.CharField(max_length=50)
    cover_image = models.ImageField(
        upload_to="brand_covers/", null=True, blank=True
    )  # Add cover_image field

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "brands"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
class Sell_Page_Product(models.Model):
    id = models.AutoField(primary_key=True)
    subCategory = models.ForeignKey(
        SubCategory,
        related_name="sell_page_products",
        on_delete=models.CASCADE,
        default=1
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)  # English name
    အမည် = models.CharField(max_length=255)  # Burmese name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # English price
    စျေး = models.DecimalField(max_digits=10, decimal_places=2) # Burmese price
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    လျှော့စျေး = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    အဓိကပုံ = models.ImageField(upload_to='products/images/', null=True, blank=True)
    secondary_image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    ဒုတိယပုံ = models.ImageField(upload_to='products/images/', null=True, blank=True)
    description = RichTextField(null = True)  # English description
    ဖော်ပြချက် = RichTextField(null = True)  # Burmese description
    is_burmese = models.BooleanField(default=False)  # Identify if the product is Burmese

    def get_price(self):
        return self.sale_price if self.is_sale else self.price

    def str(self):
        # Show the name based on the language
        return self.name if not self.is_burmese else self.အမည်


class Buy_Page_Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=7)
    subCategory = models.ForeignKey(
        SubCategory, related_name="buy_page_products", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1
    )  # Corrected field name
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    description = RichTextField(null = True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=7)
    main_image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    secondary_image = models.ImageField(upload_to="products/", null=True, blank=True)
    extra_image1 = models.ImageField(upload_to="products/", null=True, blank=True)
    extra_image2 = models.ImageField(upload_to="products/", null=True, blank=True)
    key_ingredients = models.TextField(blank=True, null=True)
    how_to_use = models.TextField(blank=True, null=True)
    environmentalImpact =  models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def get_price(self):
        return self.sale_price if self.is_sale else self.price
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


from django.utils import timezone
from django.conf import settings


# Customer Orders
class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    customer_name = models.CharField(max_length=100, default="Default Name")
    customer_address = models.CharField(max_length=255, default="Default Address")
    customer_city = models.CharField(max_length=50, default="Default City")
    customer_phone = models.CharField(max_length=15, default="Default Phone")
    created_at = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
   

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Buy_Page_Product", on_delete=models.CASCADE, null=True, blank=True)
    product_sell = models.ForeignKey("Sell_Page_Product", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name if self.product else self.product_sell.name} ({self.quantity}) in Order {self.order.id}"
        
    
####################### K M T profile and Login Logout #######################################
# Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=20000, blank=True, null=True)
    old_wishlist = models.CharField(max_length=20000, blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Buy_Page_Product, on_delete=models.CASCADE, null=True, blank=True)
    product_sell = models.ForeignKey(Sell_Page_Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    cart_type = models.CharField(max_length=10, choices=(("buy", "Buy"), ("sell", "Sell"), ("b_buyview", "b_buyview"), ("bsell_view", "bsell_view")), default="buy")
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        if self.cart_type == "buy" and self.product:
            return self.quantity * self.product.get_price()
        elif self.cart_type == "sell" and self.product_sell:
            return self.quantity * self.product_sell.get_price()
        elif self.cart_type == "b_buyview" and self.product:
            return self.quantity * self.product.get_price()
        elif self.cart_type == "bsell_view" and self.product_sell:
            return self.quantity * self.product_sell.get_price()
        return 0

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Buy_Page_Product, on_delete=models.CASCADE, null=True, blank=True)  # For buy page
    product_sell = models.ForeignKey(Sell_Page_Product, on_delete=models.CASCADE, null=True, blank=True)  # For sell page
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "product"]

    def str(self):
        if self.cart_type == "buy" and self.product:
            return f"{self.user.username}'s wishlist - {self.product.name}"
        elif self.cart_type == "sell" and self.product_sell:
            return f"{self.user.username}'s wishlist - {self.product_sell.name}"
        return 0
        
def ShippingInfo(request):
    return render(request, 'ShippingInfoV2.html', {})

from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name

