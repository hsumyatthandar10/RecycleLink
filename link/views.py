from django.shortcuts import render, redirect, get_object_or_404
from .models import Buy_Page_Product
from .models import Sell_Page_Product
from .models import Category, Order, OrderItem
from .models import SubCategory
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Cart
from .models import Wishlist
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def home(request):
    request.session.setdefault('language', 'en')
    if request.session['language'] == 'en':
        return render(request, 'home.html')
    else:
        return render(request, 'bhome.html')

from django.db.models import Sum
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Buy_Page_Product, Cart
from django.db.models import Sum

def buy(request):
    # Redirect anonymous users to the login page
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view and manage your buy cart.")
        return redirect('login')

    # Fetch products and cart items for authenticated users
    buy_page_products = Buy_Page_Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user, cart_type="buy")
    paginator = Paginator(buy_page_products, 5000)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_total = cart_items.aggregate(total_price=Sum('quantity') * Sum('product__price'))['total_price'] or 0
    cart_count = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'buy_page_products': buy_page_products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,  # Pass the total count to the template
    }
    
    return render(request, 'buy.html', {'buy_page_products': buy_page_products, 'page_obj':page_obj, 'categories': categories})
# def buy(request):
#     buy_page_products = Buy_Page_Product.objects.all()
#     categories = Category.objects.all()
#     return render(request, 'buy.html', {'buy_page_products': buy_page_products, 'categories': categories})

def sell(request):
    # Redirect anonymous users to the login page
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view and manage your sell cart.")
        return redirect('login')

    sell_page_products = Sell_Page_Product.objects.filter(is_burmese=False)
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user, cart_type="sell")

    # Calculate the total price and total quantity for sell cart
    cart_total = cart_items.aggregate(total_price=Sum('quantity') * Sum('product_sell__price'))['total_price'] or 0
    cart_count1 = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'sell_page_products': sell_page_products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count1': cart_count1,  # Pass the total count to the template
        'categories': categories,
    }
    return render(request, 'sell.html', context)

# def sell(request):
#     # Fetch only English products
#     sell_page_products = Sell_Page_Product.objects.filter(is_burmese=False)
#     categories = Category.objects.all()
#     return render(request, 'sell.html', {
#         'sell_page_products': sell_page_products,
#         'categories': categories,
#     })



def about_us(request):
    return render(request, 'aboutus.html')

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

def contact_us(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not all([first_name, last_name, email, phone, message]):
            messages.error(request, 'Please fill out all fields before submitting your message.')
            return render(request, 'contact.html')

        # Sending the email
        try:
            send_mail(
                subject=f"Message from {first_name} {last_name}",
                message=message,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Email will be sent to your default email
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return render(request, 'contact.html')

    return render(request, 'contact.html')


def user_guideline(request):
    return render(request, 'userGuideline.html')

def B_UserGuideLineview(request):
    return render(request, 'B_UserGuideLine.html')

def video_view(request):
    return render(request, 'video.html')

def Bvideo_view(request):
    return render(request, 'B_video.html')

def Post_view(request):
    return render(request, 'Post.html')

def Allpost_view(request):
    return render(request, 'Allpost.html')

def sell_productDetail(request, product_id):
    sell_page_products = get_object_or_404(Sell_Page_Product, id=product_id)
    return render (request, 'sellProductDetail.html', {'product': sell_page_products})

def buy_productDetail(request, product_id):
    buy_page_products = get_object_or_404(Buy_Page_Product, id=product_id)
    return render (request, 'ProductDetail.html', {'product': buy_page_products})

from django.db.models import Q

def product_filter_sell(request):
    sort_by = request.GET.get('sort', 'default')
    selected_categories = request.GET.getlist('category')  # Get selected categories from query parameters
    print(f"Selected categories: {selected_categories}")
    sell_page_products = Sell_Page_Product.objects.all()
    if selected_categories:
        sell_page_products = sell_page_products.filter(
            Q(category__name__in=selected_categories) | Q(brand__name__in=selected_categories)
        )
    if sort_by == 'name-asc':
        sell_page_products = sell_page_products.order_by('name')
    elif sort_by == 'name-desc':
        sell_page_products = sell_page_products.order_by('-name')
    elif sort_by == 'price-asc':
        sell_page_products = sell_page_products.order_by('price')
    elif sort_by == 'price-desc':
        sell_page_products = sell_page_products.order_by('-price')

    context = {
        'sell_page_products': sell_page_products,
    }
    return render(request, 'sell.html', context)


def product_filter_buy(request):
    sort_by = request.GET.get('sort', 'default')
    selected_categories = request.GET.getlist('category')  # Get selected categories from query parameters
    print(f"Selected categories: {selected_categories}")
    buy_page_products = Buy_Page_Product.objects.all()
    if selected_categories:
        buy_page_products = buy_page_products.filter(
            Q(category__name__in=selected_categories) | Q(brand__name__in=selected_categories)
        )
    if sort_by == 'name-asc':
        buy_page_products = buy_page_products.order_by('name')
    elif sort_by == 'name-desc':
        buy_page_products = buy_page_products.order_by('-name')
    elif sort_by == 'price-asc':
        buy_page_products = buy_page_products.order_by('price')
    elif sort_by == 'price-desc':
        buy_page_products = buy_page_products.order_by('-price')

    context = {
        'buy_page_products': buy_page_products,
    }
    return render(request, 'buy.html', context)

def sell_product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    sell_page_products = Sell_Page_Product.objects.filter(category=category)
    categories = Category.objects.all()
    print(f"Category: {category}, Products: {sell_page_products}")

    # Pass the data to the template
    return render(request, 'sell.html', {
        'sell_page_products': sell_page_products,
        'categories': categories,
        'active_category': category,
    })


def sell_product_list_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    sell_page_products = Sell_Page_Product.objects.filter(subCategory=subcategory)
    categories = Category.objects.all()
    
    return render(request, 'sell.html', {
        'sell_page_products': sell_page_products,
        'categories': categories,
        'active_subcategory': subcategory,  # Pass the active subcategory for highlighting
    })
    
def buy_product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    buy_page_products = Buy_Page_Product.objects.filter(category=category)
    categories = Category.objects.all()
    print(f"Category: {category}, Products: {buy_page_products}")

    # Pass the data to the template
    return render(request, 'buy.html', {
        'buy_page_products': buy_page_products,
        'categories': categories,
        'active_category': category,
    })


def buy_product_list_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    buy_page_products = Buy_Page_Product.objects.filter(subCategory=subcategory)
    categories = Category.objects.all()
    
    return render(request, 'buy.html', {
        'buy_page_products': buy_page_products,
        'categories': categories,
        'active_subcategory': subcategory,  # Pass the active subcategory for highlighting
    })

# def search(request):
#     if request.method == "POST":
#         searched = request.POST.get('searched', '')
#         if searched:
#             results = Buy_Page_Product.objects.filter(name__icontains=searched)
#             return render(request, 'buy.html', {'searched': searched, 'results': results})
#         else:
#             return render(request, 'buy.html', {'error': 'No search term entered'})
#     return render(request, 'buy.html', {'searched': None, 'results': None})

# def search(request):
#     if request.method == "POST":
#         searched = request.POST.get('searched', '')
#         if searched:
#             results = Buy_Page_Product.objects.filter(name__icontains=searched)
#             return render(request, 'B_buy.html', {'searched': searched, 'results': results})
#         else:
#             return render(request, 'B_buy.html', {'error': 'No search term entered'})
#     return render(request, 'B_buy.html', {'searched': None, 'results': None})

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        language = request.POST.get('language', 'en')  # Default to English if no language is specified
        
        if searched:
            results = Buy_Page_Product.objects.filter(name__icontains=searched)
            template = 'buy.html' if language == 'en' else 'B_buy.html'
            return render(request, template, {'searched': searched, 'results': results})
        else:
            error_message = 'No search term entered' if language == 'en' else 'ဘာသုံးလို့မရပါဘူး'
            template = 'buy.html' if language == 'en' else 'B_buy.html'
            return render(request, template, {'error': error_message})
    else:
        # Handle GET request
        language = request.GET.get('language', 'en')  # Default to English if no language is specified
        template = 'buy.html' if language == 'en' else 'B_buy.html'
        return render(request, template, {'searched': None, 'results': None})


def some_view(request):
    categories = Category.objects.prefetch_related('ccategories').all()
    return render(request, 'your_template.html', {
        'categories': categories,
    })
    

def product_category_sell(request, category_name):
    sell_page_products = Sell_Page_Product.objects.filter(category__name=category_name)
    context = {
        'sell_page_products': sell_page_products,
        'category_name': category_name,
    }
    return render(request, 'sell.html', context)


# Khin's Login Logout #
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Check for empty fields
        if not username or not email or not password or not phone:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')

        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account: ' + str(e))
            return render(request, 'signup.html')

    return render(request, 'signup.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    """
    Logs out the user and redirects them to the home page or login page.
    """
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your desired redirect page


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    posts = request.session.get("posts", [])  # Retrieve posts from session
    return render(request, "profile.html", {"posts": posts})

@login_required
def delete_post(request, index):
    posts = request.session.get("posts", [])

    if 0 <= index < len(posts):
        del posts[index]  # Remove the selected post
        request.session["posts"] = posts
        request.session.modified = True  # Ensure session updates

    return redirect("profile")  



def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')
        cart_type = data.get('cart_type', 'buy')  # Default to 'buy'

        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'})

        try:
            user = request.user

            # Determine product and cart type
            if cart_type == 'buy':
                product = get_object_or_404(Buy_Page_Product, id=product_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=user, product=product, cart_type="buy"
                )
            elif cart_type == 'sell':
                product = get_object_or_404(Sell_Page_Product, id=product_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=user, product_sell=product, cart_type="sell"
                )
            elif cart_type == 'b_buyview':
                product = get_object_or_404(Buy_Page_Product, id=product_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=user, product=product, cart_type="b_buyview"
                )
            elif cart_type == 'bsell_view':
                product = get_object_or_404(Sell_Page_Product, id=product_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=user, product_sell=product, cart_type="bsell_view"
                )
            else:
                return JsonResponse({'success': False, 'error': 'Invalid cart type'})

            # Update quantity if the item already exists
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Calculate the total quantity in the cart
            cart_count = Cart.objects.filter(user=user, cart_type=cart_type).aggregate(
                total_quantity=Sum('quantity')
            )['total_quantity'] or 0

            return JsonResponse({'success': True, 'cart_count': cart_count})

        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart, Sell_Page_Product
import json

def add_to_cart1(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Sell_Page_Product, id=product_id)
        user = request.user

        # Add or update the product in the user's cart
        cart_item, created = Cart.objects.get_or_create(
            user=user, product_sell=product, cart_type="sell"
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        # Correctly calculate the cart count (sum of quantities)
        cart_count1 = Cart.objects.filter(user=user, cart_type="sell").aggregate(Sum('quantity'))['quantity__sum'] or 0
        return JsonResponse({'success': True, 'cart_count1': cart_count1})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def add_to_wishlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")

        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'})

        user = request.user

        # Handling authenticated users
        if user.is_authenticated:
            product = get_object_or_404(Buy_Page_Product, id=product_id)
            Wishlist.objects.get_or_create(user=user, product=product)
            wishlist_count = Wishlist.objects.filter(user=user).count()
        else:
            # Handling guest users with session storage
            wishlist = request.session.get("wishlist", [])
            if product_id not in wishlist:
                wishlist.append(product_id)
                request.session["wishlist"] = wishlist
            wishlist_count = len(wishlist)

        request.session['wishlist_count'] = wishlist_count
        return JsonResponse({'success': True, 'wishlist_count': wishlist_count})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
def add_to_wishlist1(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")

            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID is required'})

            user = request.user

            if user.is_authenticated:
                product = get_object_or_404(Sell_Page_Product, id=product_id)
                Wishlist.objects.get_or_create(user=user, product_sell=product)

                # ✅ Immediately fetch and return updated count
                wishlist_count1 = Wishlist.objects.filter(user=user).count()
            else:
                wishlist = request.session.get("wishlist", [])
                if product_id not in wishlist:
                    wishlist.append(product_id)
                    request.session["wishlist"] = wishlist  # ✅ Save session immediately

                wishlist_count1 = len(wishlist)

            # ✅ Ensure session is updated before returning response
            request.session['wishlist_count1'] = wishlist_count1  
            request.session.modified = True  

            return JsonResponse({'success': True, 'wishlist_count1': wishlist_count1})  # ✅ Send correct count immediately

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    every_other_order = orders[::2]  
    paginator = Paginator(every_other_order, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'OrderHistory.html', {'page_obj': page_obj})

from django.shortcuts import get_object_or_404, render
from .models import Order, OrderItem
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    ordered_items = OrderItem.objects.filter(order=order)

    print(f"✅ Order ID: {order.id}")
    print(f"🔍 Ordered Items: {ordered_items}")

    if not ordered_items:
        print("⚠️ No order items found!")

    return render(request, "Voucher.html", {"order": order, "ordered_items": ordered_items, 'order_id': order_id})


from django.http import JsonResponse
from .models import Cart

def get_cart_items(request):
    print("get_cart_items function triggered")  # Debugging step ✅

    try:
        cart_type = request.GET.get('cart_type')
        print(f"Cart Type Received: {cart_type}")  # ✅ Print received cart_type

        if cart_type not in ['buy', 'sell']:  
            return JsonResponse({'success': False, 'error': 'Invalid cart type'})

        cart_items = Cart.objects.filter(user=request.user, cart_type=cart_type)
        print(f"Cart Items Found: {cart_items}")  # Debugging step ✅

        items = []
        total = 0  # ✅ Ensure total is initialized

        for item in cart_items:
            product = item.product_sell if cart_type == 'sell' else item.product
            if not product:
                continue  # Skip invalid products

            item_price = float(product.sale_price if product.sale_price else product.price)
            total += item.quantity * item_price  # ✅ Ensure correct calculation

            print(f"Processing Item: {product.name}, Quantity: {item.quantity}, Price: {item_price}")  # ✅ Debug

            items.append({
                'id': item.id,
                'name': product.name,
                'price': item_price,
                'quantity': item.quantity,
                'image_url': product.main_image.url if product.main_image else '',
            })

        print(f"Final Total Sent: {total}")  # ✅ Check final total before sending

        return JsonResponse({'success': True, 'items': items, 'total': float(total)})

    except Exception as e:
        print(f"Error in get_cart_items: {str(e)}")  # ✅ Debug errors
        return JsonResponse({'success': False, 'error': str(e)})
    


from django.http import JsonResponse
from .models import Cart

def update_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        cart_type = data.get('cart_type', 'sell')

        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user, cart_type=cart_type)

            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()  # Remove the item if quantity becomes zero
            elif action == 'remove':
                cart_item.delete()  # Remove the item entirely

            return JsonResponse({'success': True})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.http import JsonResponse

def get_cart_counts(request):
    if not request.user.is_authenticated:
        return JsonResponse({'buy_cart_count': 0, 'sell_cart_count': 0, 'bbuy_cart_count': 0, 'bsell_cart_count': 0})

    buy_cart_count = Cart.objects.filter(user=request.user, cart_type="buy").aggregate(total=Sum('quantity'))['total'] or 0
    sell_cart_count = Cart.objects.filter(user=request.user, cart_type="sell").aggregate(total=Sum('quantity'))['total'] or 0
    
    return JsonResponse({'buy_cart_count': buy_cart_count, 'sell_cart_count': sell_cart_count})

# Form Hus Myat
def bhome_view(request):
    return render(request, 'Bhome.html')

def toggle_language(request, lang):
    
    if lang in ['en', 'my']:
        request.session['language'] = lang
    return redirect('home')

# def bsell_view(request):
#     # Fetch only Burmese products
#     sell_page_products = Sell_Page_Product.objects.filter(is_burmese=False)
#     categories = Category.objects.all()
#     return render(request, 'Bsell.html', {
#         'sell_page_products': sell_page_products,
#         'categories': categories,
#     })
    
def bsell_view(request):
    # Redirect anonymous users to the login page
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view and manage your sell cart.")
        return redirect('login')

    sell_page_products = Sell_Page_Product.objects.filter(is_burmese=False)
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user, cart_type="bsell_view")

    # Calculate the total price and total quantity for sell cart
    cart_total = cart_items.aggregate(total_price=Sum('quantity') * Sum('product_sell__price'))['total_price'] or 0
    cart_count1 = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'sell_page_products': sell_page_products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count1': cart_count1,  # Pass the total count to the template
        'categories': categories,
    }
    return render(request, 'Bsell.html', context)

# def b_buyview(request):
#     buy_page_products = Buy_Page_Product.objects.all()
#     categories = Category.objects.all()
#     print(f"Products: {buy_page_products}")
#     print(f"Categories: {categories}")
#     return render(request, 'B_buy.html', {'buy_page_products': buy_page_products, 'categories': categories})

def b_buyview(request):
    # Redirect anonymous users to the login page
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view and manage your buy cart.")
        return redirect('login')

    # Fetch products and cart items for authenticated users
    buy_page_products = Buy_Page_Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user, cart_type="b_buyview")

    # Calculate the cart total price and total quantity
    cart_total = cart_items.aggregate(total_price=Sum('quantity') * Sum('product__price'))['total_price'] or 0
    cart_count = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'buy_page_products': buy_page_products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,  # Pass the total count to the template
        'categories': categories,
    }
    return render(request, 'B_buy.html', context)

def Bsell_productDetail(request, product_id):
    sell_page_products = get_object_or_404(Sell_Page_Product, id=product_id)
    return render (request, 'BsellProductDetail.html', {'product': sell_page_products})

def buy_productDetail_burmese(request, product_id):
    print(f"Requested Product ID: {product_id}")
    buy_page_products = get_object_or_404(Buy_Page_Product, id=product_id)
    print(f"Product Retrieved: {buy_page_products}")
    return render(request, 'BProductDetail.html', {'product': buy_page_products})

def bhome_view(request):
    return render(request, 'Bhome.html')


def bAboutus_view(request):
    return render(request, 'B_aboutus.html')


def B_contactusview(request):
    return render(request, 'B_contactus.html')

def product_filter_sell_burmese(request):
    sort_by = request.GET.get('sort', 'default')
    selected_categories = request.GET.getlist('category')  # Get selected categories from query parameters
    print(f"Selected categories: {selected_categories}")
    sell_page_products = Sell_Page_Product.objects.all()
    if selected_categories:
        sell_page_products = sell_page_products.filter(
            Q(category__name__in=selected_categories) | Q(brand__name__in=selected_categories)
        )
    if sort_by == 'name-asc':
        sell_page_products = sell_page_products.order_by('name')
    elif sort_by == 'name-desc':
        sell_page_products = sell_page_products.order_by('-name')
    elif sort_by == 'price-asc':
        sell_page_products = sell_page_products.order_by('price')
    elif sort_by == 'price-desc':
        sell_page_products = sell_page_products.order_by('-price')

    context = {
        'sell_page_products': sell_page_products,
    }
    return render(request, 'Bsell.html', context)

def product_filter_buy_burmese(request):
    sort_by = request.GET.get('sort', 'default')
    selected_categories = request.GET.getlist('category')  # Get selected categories from query parameters
    print(f"Selected categories: {selected_categories}")
    buy_page_products = Buy_Page_Product.objects.all()
    if selected_categories:
        buy_page_products = buy_page_products.filter(
            Q(category__name__in=selected_categories) | Q(brand__name__in=selected_categories)
        )
    if sort_by == 'name-asc':
        buy_page_products = buy_page_products.order_by('name')
    elif sort_by == 'name-desc':
        buy_page_products = buy_page_products.order_by('-name')
    elif sort_by == 'price-asc':
        buy_page_products = buy_page_products.order_by('price')
    elif sort_by == 'price-desc':
        buy_page_products = buy_page_products.order_by('-price')

    context = {
        'buy_page_products': buy_page_products,
    }
    return render(request, 'B_buy.html', context)

def sell_product_list_by_category_burmese(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    sell_page_products = Sell_Page_Product.objects.filter(category=category)
    categories = Category.objects.all()
    print(f"Category: {category}, Products: {sell_page_products}")

    # Pass the data to the template
    return render(request, 'Bsell.html', {
        'sell_page_products': sell_page_products,
        'categories': categories,
        'active_category': category,
    })

def sell_product_list_by_subcategory_burmese(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    sell_page_products = Sell_Page_Product.objects.filter(subCategory=subcategory)
    categories = Category.objects.all()
    
    return render(request, 'Bsell.html', {
        'sell_page_products': sell_page_products,
        'categories': categories,
        'active_subcategory': subcategory,  # Pass the active subcategory for highlighting
    })

def buy_product_list_by_category_burmese(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    buy_page_products = Buy_Page_Product.objects.filter(category=category)
    categories = Category.objects.all()
    print(f"Category: {category}, Products: {buy_page_products}")

    # Pass the data to the template
    return render(request, 'B_buy.html', {
        'buy_page_products': buy_page_products,
        'categories': categories,
        'active_category': category,
    })

def buy_product_list_by_subcategory_burmese(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    buy_page_products = Buy_Page_Product.objects.filter(subCategory=subcategory)
    categories = Category.objects.all()
    
    return render(request, 'B_buy.html', {
        'buy_page_products': buy_page_products,
        'categories': categories,
        'active_subcategory': subcategory,  # Pass the active subcategory for highlighting
    })

def product_category_sell_burmese(request, category_name):
    sell_page_products = Sell_Page_Product.objects.filter(category__name=category_name)
    context = {
        'sell_page_products': sell_page_products,
        'category_name': category_name,
    }
    return render(request, 'Bsell.html', context)


def wishlist_view(request):
    if request.user.is_authenticated:
        buy_wishlist_items = Wishlist.objects.filter(user=request.user, product__isnull=False)
        sell_wishlist_items = Wishlist.objects.filter(user=request.user, product_sell__isnull=False)

        return render(request, 'wishlist.html', {
            'buy_wishlist_items': buy_wishlist_items,
            'sell_wishlist_items': sell_wishlist_items
        })
    else:
        return redirect('login')
    

from django.views.decorators.csrf import csrf_protect
@login_required
@csrf_protect
def remove_wishlist_item(request, item_id):
    if request.method == "POST":
        try:
            wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
            wishlist_item.delete()

            # Calculate the updated count
            wishlist_count = Wishlist.objects.filter(user=request.user).count()

            return JsonResponse({"success": True, "wishlist_count": wishlist_count})
        except Wishlist.DoesNotExist:
            return JsonResponse({"success": False, "error": "Wishlist item not found."})
    return JsonResponse({"success": False, "error": "Invalid request"})


def ShippingInfo(request):
    return render(request, 'ShippingInfoV2.html', {})

def LocationTracker(request):
    return render(request, 'locationTracker.html', {})


import json
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Cart, OrderItem

@csrf_exempt
@login_required
def create_order(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)

            # Get logged-in user
            customer = request.user

            # Fetch cart items for the user
            cart_items = Cart.objects.filter(user=customer)
            if not cart_items.exists():
                return JsonResponse({"success": False, "message": "Cart is empty!"})

            # Extract shipping details from frontend data
            customer_name = data.get("customer_name", customer.username)
            customer_address = data.get("customer_address", "")
            customer_city = data.get("customer_city", "Default City")
            customer_phone = data.get("customer_phone", "Default Phone")
            shipping_fee = Decimal(data.get("shipping_fee", "0"))

            # Calculate subtotal
            subtotal = sum(item.get_total() for item in cart_items)
            total = subtotal + shipping_fee

            # Create the order
            order = Order.objects.create(
                customer=customer,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_city=customer_city,
                customer_phone=customer_phone,
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                total=total,
            )

            # Now, create OrderItems for each cart item
            for cart_item in cart_items:
                if cart_item.product:  # Buy product
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.get_price(),
                    )
                elif cart_item.product_sell:  # Sell product
                    order_item = OrderItem.objects.create(
                        order=order,
                        product_sell=cart_item.product_sell,
                        quantity=cart_item.quantity,
                        price=cart_item.product_sell.get_price(),
                    )

                print(f"Order Item Created: {order_item.product or order_item.product_sell} - {order_item.quantity} pcs @ ${order_item.price}")

            # Clear the cart after order is created
            cart_items.delete()
            print("Cart cleared!")  # Debugging step ✅

            return JsonResponse({"success": True, "order_id": order.id})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})



from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Cart

def create_order_from_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return JsonResponse({'success': False, 'error': 'Cart is empty'})

    order = Order.objects.create(user=user, total=0)  # Adjust total calculation
    order_items = []

    for item in cart_items:
        product = item.product or item.product_sell
        cart_items = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.sale_price or product.price
        )
        order_items.append(cart_items)

    cart_items.delete()  # Clear cart after creating order

    return JsonResponse({'success': True, 'order_id': order.id})

from django.shortcuts import render, redirect
from .models import Cart, Order, OrderItem

def proceed_to_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return render(request, 'cart_empty.html')  # Redirect if cart is empty

    # Create a new order for the user
    order = Order.objects.create(user=request.user, total=0)

    total_price = 0

    # Loop through cart items and create order items
    for item in cart_items:
        if item.cart_type == "buy" and item.product:
            product = item.product
        elif item.cart_type == "sell" and item.product_sell:
            product = item.product_sell
        else:
            continue  # Skip if no valid product

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.price
        )
        total_price += item.quantity * product.price  # Calculate total order price

    # Update order total and save
        order.total = total_price
        order.save()

        # Clear the cart after moving items to order
        cart_items.delete()

        return redirect("order_success", order_id=order.id)

    return render(request, "ShippingInfoV2.html")

import json
import random
import nltk
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# # Ensure NLTK data is downloaded
# nltk.download('punkt')
# nltk.download('wordnet')

responses = {
    "hello": ["Hi there! How can I help you? 😊"],
    "hi": ["Hello there! How can I help you? 😊"],
    "fine": ["I'm just a bot, but I'm doing great!"],
    "site": [
        "This site facilitates selling recycled products and buying recycled waste.",
        "RecycleLink is an online platform where users can sell recyclable materials, and customers can buy products made from recycled materials."
    ],
    "aim": [
        "RecycleLink aims to be Myanmar's leading platform for reducing waste, repurposing materials, and creating a healthier environment."
    ],
    "provide": [
        "RecycleLink provides a solution for recycling and reusing materials through three services:\n"
        "- Buying recyclables: We purchase plastic bags, bottles, and paper to ensure proper recycling.\n"
        "- Selling recycled products: Customers can explore and buy eco-friendly products.\n"
        "- Connecting communities: Users can post about recyclable materials they want to sell or buy."
    ],
    "choose": [
        "RecycleLink stands out because:\n"
        "- **Sustainability First:** We focus on reducing waste and promoting eco-friendly practices.\n"
        "- **Convenient Solutions:** We offer delivery services and easy communication to make recycling effortless.\n"
        "- **Empowering Communities:** We connect people who care about the environment and encourage collective action."
    ],
    "team": [
        "Meet our team:\n"
        "- **Khin Myat Thu (Project Manager):** Ensures smooth operations and platform development.\n"
        "- **Lin Lae Phyu (Lead Developer):** Builds and maintains the website for a seamless experience.\n"
        "- **Hsu Myat Thandar (Marketing & Customer Support):** Engages users and promotes the platform."
    ],
    "recyclelink": [
        "RecycleLink is an online platform where users can sell recyclable materials like plastic bottles and paper. "
        "Admins buy these materials, and customers can also purchase products made from recycled items."
    ],
    "recycle link": [
        "RecycleLink is an online platform where users can sell recyclable materials like plastic bottles and paper. "
        "Admins buy these materials, and customers can also purchase products made from recycled items."
    ],
    "sell": [
        "To sell your recyclable items:\n"
        "- Click on the 'Sell' tab.\n"
        "- Check the limited amount (we only accept the amount of >= 30000 MMK cuz of transportation).\n"
        "- Use Location Tracker to find the nearest admin.\n"
    ],
    "buy": [
        "Customers can browse and purchase eco-friendly products made from recycled materials, such as:\n"
        "- Reusable bags\n"
        "- Furniture\n"
        "- Decorative items"
    ],
    "work": [
        "Payments for sold recyclable items are credited to the user’s account. "
        "Buyers can purchase products using online payment methods or cash on delivery (if available)."
    ],
    "payment process": [
        "Payments for sold recyclable items are credited to the user’s account. "
        "Buyers can purchase products using online payment methods or cash on delivery (if available)."
    ],
    "quality check": [
        "Yes, admins verify the quality and type of recyclable materials before purchasing to ensure they meet recycling standards."
    ],
    "quality": [
        "Yes, admins verify the quality and type of recyclable materials before purchasing to ensure they meet recycling standards."
    ],
    "use": [
        "RecycleLink promotes environmental sustainability by reducing waste and encouraging the reuse of materials. "
        "It also allows users to earn money and buy eco-friendly products."
    ],
    "bye": ["Goodbye! Have a great day! 🌿"],
    
    # Burmese translations
    "မင်္ဂလာပါ": ["မင်္ဂလာပါ! သင့်ကိုဘယ်လိုကူညီပေးရမလဲ။"],
    "နေကောင်းလား": ["ကျွန်ုပ်သည် chatbot တစ်ခုဖြစ်သည်။ သို့သော်၊ ကျွန်ုပ်ကောင်းမွန်နေပါသည်။"],
    "ဘယ်ကြောင့် RecycleLink ကိုအသုံးပြုသင့်သလဲ": [
        "RecycleLink သည် စာရင်းပြုစုထားသော ပတ်ဝန်းကျင်ထိန်းသိမ်းမှုကို မြှင့်တင်ရန် ရည်ရွယ်ပါသည်။ "
        "ထို့ကြောင့် သင့်အတွက် အကျိုးကျေးဇူးရှိသည်။"
    ],
    "အကျိုးကျေးဇူး": [
        "RecycleLink သည် သုံးစွဲသူများကို ကမ္ဘာမြေကြီး ကျန်းမာဖွံ့ဖြိုး စေရန် ကူညီပါသည်။ "
        "သင်သည် အသုံးပြုနိုင်သော ပစ္စည်းများကို ပြန်လည်အသုံးပြု၍ ငွေရှာနိုင်သည်။"
    ],
    "ရည်မှန်းချက်": [
        "RecycleLink သည် မြန်မာနိုင်ငံ၏ အမှိုက်လျှော့ချခြင်း၊ ပစ္စည်းများကို ပြန်လည်အသုံးပြုနိုင်စေရန်နှင့် ပိုမိုကျန်းမာသော ပတ်ဝန်းကျင်ဖန်တီးခြင်းကို ရည်ရွယ်ထားပါသည်။"
    ],
    "ရည်ရွယ်ချက်": [
        "RecycleLink သည် မြန်မာနိုင်ငံ၏ အမှိုက်လျှော့ချခြင်း၊ ပစ္စည်းများကို ပြန်လည်အသုံးပြုနိုင်စေရန်နှင့် ပိုမိုကျန်းမာသော ပတ်ဝန်းကျင်ဖန်တီးခြင်းကို ရည်ရွယ်ထားပါသည်။"
    ],
    "ပံ့ပိုး": [
        "RecycleLink သည် ပြန်လည်အသုံးပြုခြင်းနှင့် ပြန်လည်စုပြုံခြင်းအတွက် ဖြေရှင်းမှုတစ်ခုကို ပံ့ပိုးပေးပါသည်။\n"
        "- **အမှိုက်အများစုကို ဝယ်ယူခြင်း**: ပလပ်စတစ်အိတ်၊ ပုလင်းများ၊ စက္ကူများကို ကျွန်ုပ်တို့ဝယ်ယူ၍ မှန်ကန်သော ပြန်လည်အသုံးပြုမှုကိုသေချာစေရန်။\n"
        "- **ပြန်လည်အသုံးပြုထားသော ထုတ်ကုန်များ ရောင်းဝယ်ခြင်း**: စွမ်းအင်ချွေတာသောထုတ်ကုန်များကို ဝယ်ယူနိုင်သည်။\n"
        "- **လူမှုအသိုင်းအဝိုင်း ချိတ်ဆက်မှု**: အသုံးပြုနိုင်သော အမှိုက်များကို ရောင်းလိုသောသူများနှင့် ဝယ်လိုသောသူများကို ချိတ်ဆက်ပေးသည်။"
    ],
    "ရွေးချယ်": [
        "RecycleLink သည် အထူးသဖြင့်:\n"
        "- **သန့်ရှင်းသော သဘာဝပတ်ဝန်းကျင်**: ကျွန်ုပ်တို့သည် အမှိုက်လျှော့ချခြင်းနှင့် သဘာဝပတ်ဝန်းကျင်ကို ထိန်းသိမ်းရေးကို ဦးစားပေးပါသည်။\n"
        "- **အဆင်ပြေမှု**: ပို့ဆောင်မှု၊ ဝန်ဆောင်မှုများနှင့် ပိုမိုလွယ်ကူသော ဆက်သွယ်မှုများဖြင့် ပြန်လည်အသုံးပြုမှုကို လွယ်ကူစေသည်။\n"
        "- **အသိုင်းအဝိုင်း အားကောင်းမှု**: သဘာဝပတ်ဝန်းကျင်ကို ဦးစားပေးသော လူများကို ချိတ်ဆက်ပေးပြီး ပိုမိုကောင်းမွန်သော လုပ်ဆောင်မှုများကို တိုက်တွန်းပေးပါသည်။"
    ],
    "အဖွဲ့": [
        "ကျွန်ုပ်တို့၏အသင်းအဖွဲ့:\n"
        "- **ခင်မြတ်သူ (Project Manager)**: အင်တာနက်ပလက်ဖောင်းကို စီမံခန့်ခွဲပြီး စနစ်တကျ လည်ပတ်နိုင်ရန် စီစဉ်ပါသည်။\n"
        "- **လင်းလဲ့ဖြူ (Lead Developer)**: ဝဘ်ဆိုက်ကို တည်ဆောက်ပြီး အသုံးပြုရလွယ်ကူစေရန် ပြုပြင်ထိန်းသိမ်းသည်။\n"
        "- **ဆုမြတ်သန္တာ (Marketing & Customer Support)**: အသုံးပြုသူများနှင့် ဆက်သွယ်ပြီး အထောက်အပံ့ပေးပါသည်။"
    ],
    "အဖွဲ့ဝင်": [
        "ကျွန်ုပ်တို့၏အသင်းအဖွဲ့:\n"
        "- **ခင်မြတ်သူ (Project Manager)**: အင်တာနက်ပလက်ဖောင်းကို စီမံခန့်ခွဲပြီး စနစ်တကျ လည်ပတ်နိုင်ရန် စီစဉ်ပါသည်။\n"
        "- **လင်းလဲ့ဖြူ (Lead Developer)**: ဝဘ်ဆိုက်ကို တည်ဆောက်ပြီး အသုံးပြုရလွယ်ကူစေရန် ပြုပြင်ထိန်းသိမ်းသည်။\n"
        "- **ဆုမြတ်သန္တာ (Marketing & Customer Support)**: အသုံးပြုသူများနှင့် ဆက်သွယ်ပြီး အထောက်အပံ့ပေးပါသည်။"
    ],
    "ဘာလဲ": [
        "RecycleLink သည် အသုံးပြုနိုင်သော ပလပ်စတစ်ပုလင်းများနှင့် စက္ကူများကို ရောင်းချနိုင်သော အွန်လိုင်းပလက်ဖောင်းတစ်ခုဖြစ်သည်။ "
        "Admin များသည် ဤပစ္စည်းများကို ဝယ်ယူပြီး ပြန်လည်အသုံးပြုထားသော ထုတ်ကုန်များကို ဝယ်ယူနိုင်ပါသည်။"
    ],
    "ရောင်း": [
        "သင့်ရဲ့ ပြန်လည်အသုံးပြုနိုင်သော ပစ္စည်းများကို ရောင်းချရန်:\n"
        "- 'ရောင်းမည်' ခလုတ်ကို နှိပ်ပါ။\n"
        "- အနည်းဆုံး ငွေပမာဏကို စစ်ဆေးပါ (သယ်ယူပို့ဆောင်မှုကြောင့် 30,000 MMK နှင့်အထက်သာ လက်ခံပါသည်)။\n"
        "- နီးစပ်သော Admin ကို ရှာဖွေရန် တည်နေရာထောက်လှမ်းမှု (Location Tracker) ကို အသုံးပြုပါ။"
    ],
    "ဝယ်": [
        "သုံးစွဲသူများသည် ပြန်လည်အသုံးပြုထားသော ထုတ်ကုန်များကို ဝယ်ယူနိုင်ပါသည်။\n"
        "- ပြန်လည်အသုံးပြုနိုင်သော အိတ်များ\n"
        "- အိမ်တွင်းပရိဘောဂများ\n"
        "- အလှဆင်ပစ္စည်းများ"
    ],
    "ငွေပေးချေမှု": [
        "ရောင်းချထားသော ပစ္စည်းများအတွက် ငွေပေးချေမှုသည် သုံးစွဲသူ၏အကောင့်သို့ အလိုအလျှောက် အသွင်းပြုလုပ်မည်။ "
        "ဝယ်သူများသည် အွန်လိုင်းငွေပေးချေမှုစနစ်များ သို့မဟုတ် ငွေသားဖြင့် ပို့ဆောင်မှုအခါဝယ်ယူနိုင်ပါသည်။"
    ],
    "ငွေ": [
        "ရောင်းချထားသော ပစ္စည်းများအတွက် ငွေပေးချေမှုသည် သုံးစွဲသူ၏အကောင့်သို့ အလိုအလျှောက်အသွင်းပြုလုပ်မည်။ "
        "ဝယ်သူများသည် အွန်လိုင်းငွေပေးချေမှုစနစ်များ သို့မဟုတ် ငွေသားဖြင့် ပို့ဆောင်မှုအခါဝယ်ယူနိုင်ပါသည်။"
    ],
    "အရည်အသွေး": [
        "ဟုတ်ပါတယ်။ Admin များသည် ပြန်လည်အသုံးပြုနိုင်သော ပစ္စည်းများ၏ အရည်အသွေးကို စစ်ဆေးပြီးမှ ဝယ်ယူပါသည်။"
    ],
    "ဘာကြောင့် သုံး": [
        "RecycleLink သည် သဘာဝပတ်ဝန်းကျင်ထိန်းသိမ်းမှုကို အထူးပြု၍ အမှိုက်များကို လျှော့ချနိုင်စေပြီး၊ "
        "ပြန်လည်အသုံးပြုမှုအား မြှင့်တင်နိုင်သည့် ပလက်ဖောင်းတစ်ခုဖြစ်ပါသည်။ "
        "ထို့အပြင် အသုံးပြုသူများသည် ငွေရှာနိုင်ပြီး သဘာဝပတ်ဝန်းကျင်ထိန်းသိမ်းထားသော ထုတ်ကုန်များကို ဝယ်ယူနိုင်ပါသည်။"
    ],
    "တာ့တာ": ["နောက်မှတွေ့ကြမယ်။ သန့်ရှင်းသော သဘာဝပတ်ဝန်းကျင်မှာ နေထိုင်လိုက်ကြပါစို့။ 🌿"]
}

def is_myanmar(text):
    """Detects if the text is likely in Myanmar language based on Unicode range."""
    for char in text:
        if "\u1000" <= char <= "\u109F":  # Myanmar Unicode range
            return True
    return False

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # Check if the input is Myanmar
    is_myan = is_myanmar(user_input)

    for key in responses:
        if is_myan and key in user_input:  # Myanmar matching (substring search)
            return random.choice(responses[key])
        elif not is_myan:  # English matching (word-based search)
            key_tokens = key.lower().split()
            user_tokens = user_input.split()
            if any(word in user_tokens for word in key_tokens):
                return random.choice(responses[key])

    # Default response
    return "တောင်းပန်ပါတယ်။ ကျွန်ုပ်၏ အချက်အလက်များတွင် မဖြေဆိုနိုင်ပါ။" if is_myan else "I'm not sure how to respond to that. Can you rephrase?"

@csrf_exempt
def chatbot_api(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)  # Ensure valid JSON
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"error": "Empty message received."}, status=400)

            bot_reply = chatbot_response(user_message)
            return JsonResponse({"response": bot_reply}, status=200)
        
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Server Error: {str(e)}"}, status=500)
    
def check_stock(request, product_id):
    try:
        product = Buy_Page_Product.objects.get(id=product_id)
        return JsonResponse({"stock": product.stock})
    except Buy_Page_Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    
def review(request):
    return render(request, 'review.html')
def Breview(request):
    return render(request, 'Breview.html')

# Location Tracker
from django.shortcuts import render
from django.http import JsonResponse
from .models import Supplier  # Assuming you have a Supplier model
from math import radians, cos, sin, sqrt, atan2

# Function to calculate distance between two coordinates (Haversine Formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

def find_nearest_supplier(request):
    seller_lat = request.GET.get('lat')
    seller_lng = request.GET.get('lng')

    if not seller_lat or not seller_lng:
        return JsonResponse({"error": "Seller location is missing!"}, status=400)

    seller_lat = float(seller_lat)
    seller_lng = float(seller_lng)

    suppliers = Supplier.objects.all()
    nearest_supplier = None
    min_distance = float('inf')

    for supplier in suppliers:
        distance = calculate_distance(seller_lat, seller_lng, supplier.latitude, supplier.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_supplier = supplier

    if nearest_supplier:
        return JsonResponse({
            "name": nearest_supplier.name,
            "phone": nearest_supplier.phone,
            "latitude": nearest_supplier.latitude,
            "longitude": nearest_supplier.longitude,
            "distance_km": min_distance,
            "time_min": int(min_distance / 0.5)  # Example: Approximate time to supplier (assuming 30 km/h speed)
        })
    else:
        return JsonResponse({"error": "No supplier found"}, status=404)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Supplier

def get_suppliers(request):
    suppliers = Supplier.objects.values("name", "phone", "latitude", "longitude")
    return JsonResponse(list(suppliers), safe=False)

@csrf_exempt
def update_supplier_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get("phone")  # Get phone number dynamically
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if not phone:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            supplier = Supplier.objects.filter(phone=phone).first()
            if not supplier:
                return JsonResponse({"error": "Supplier not found"}, status=404)

            # Update supplier location
            supplier.latitude = latitude
            supplier.longitude = longitude
            supplier.save()

            return JsonResponse({"message": "Location updated successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)




def supplier_tracker(request):
    return render(request, 'supplier_tracker.html')
from django.shortcuts import get_object_or_404

def locationTracker(request):
    supplier_phone = request.user.supplier.phone if hasattr(request.user, 'supplier') else None
    print("Supplier Phone:", supplier_phone)  # Debugging
    return render(request, 'supplier_tracker.html', {'supplier_phone': supplier_phone})