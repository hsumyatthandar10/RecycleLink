from django.contrib import admin
from .models import Category, Brand, Sell_Page_Product, Buy_Page_Product, Order, Profile, OrderItem, SubCategory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Sell_Page_Product, Buy_Page_Product

@admin.register(Sell_Page_Product)
class SellPageProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_sale')

@admin.register(Buy_Page_Product)
class BuyPageProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_sale", "sale_price")
    list_editable = ("stock",)

# Register Order with custom admin options
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_address', 'customer_city', 'customer_phone', 'subtotal', 'shipping_fee', 'total', 'created_at')  # Added 'id' for Order ID
    search_fields = ('id', 'customer_name', 'customer_address', 'customer_city', 'customer_phone')  # Use 'id' instead of 'order__id'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'get_order_id', 'get_customer_name', 'get_product_name', 'quantity', 'price')  # Added 'get_order_id' and 'get_customer_name'
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else "N/A"
    get_product_name.short_description = "Product Name"

    def get_order_id(self, obj):
        return obj.order.id if obj.order else "N/A"
    get_order_id.short_description = "Order ID"

    def get_customer_name(self, obj):
        return obj.order.customer_name if obj.order else "N/A"
    get_customer_name.short_description = "Customer Name"


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Profile)
#################### K M T build profile #######################
class ProfileInline(admin.StackedInline):
    model = Profile

# Use get_user_model() to get the user model
User = get_user_model()

# Define custom admin for the User model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the default User model and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Brand with custom admin options
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'cover_image']

from django.contrib import admin
from .models import Supplier  # Import your model

admin.site.register(Supplier)  # Register the model
