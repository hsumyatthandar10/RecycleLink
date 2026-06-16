from django.db.models import Sum
from .models import Cart,Wishlist

def cart_context(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_total = sum(item.get_total() for item in cart_items)  # Ensure get_total() works
        cart_count = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

        return {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'cart_count': cart_count,  # Add cart count to context
            'wishlist_count': wishlist_count,  # Add wishlist count
        }
    return {'cart_items': [], 'cart_total': 0, 'cart_count': 0, 'wishlist_count': 0,}

# from .models import Cart

# def cart_context(request):
#     if request.user.is_authenticated:
#         cart_items = Cart.objects.filter(user=request.user)
#         cart_total = sum(item.get_total() for item in cart_items)
#         return {'cart_items': cart_items, 'cart_total': cart_total}
#     return {'cart_items': [], 'cart_total': 0}
