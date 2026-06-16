from django.db.models import Q

def filter_products(products, sort_by, selected_categories):
    if selected_categories:
        products = products.filter(
            Q(category__name__in=selected_categories) | Q(brand__name__in=selected_categories)
        )
    if sort_by == 'name-asc':
        products = products.order_by('name')
    elif sort_by == 'name-desc':
        products = products.order_by('-name')
    elif sort_by == 'price-asc':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')
    return products
