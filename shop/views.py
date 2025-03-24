import collections
from gc import collect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Collection
from cart.forms import CartAddProductForm
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    collections = Collection.objects.all()
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
        )
        products = products.filter(category=category)
    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products, "collections": collections},
    )


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )


def search_products(request):
    query = request.GET.get('q', '')
    if query:
        # Search in translated fields
        language = request.LANGUAGE_CODE
        products = Product.objects.filter(
            Q(translations__language_code=language) &
            (Q(translations__name__icontains=query) |
             Q(translations__description__icontains=query)) &
            Q(available=True)
        ).distinct()
    else:
        products = Product.objects.none()
    
    return render(
        request,
        'shop/product/search_results.html',
        {'products': products, 'query': query}
    )

def product_list_by_collection(request, collection_slug):
    language = request.LANGUAGE_CODE
    collection = get_object_or_404(
        Collection,
        translations__language_code=language,
        translations__slug=collection_slug,
    )
    products = collection.products.filter(available=True)
    return render(
        request,
        'shop/product/list_collection.html',
        {'collection': collection, 'products': products}
    )