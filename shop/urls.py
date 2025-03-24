from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_products, name='product_search'),
    path('collection/<slug:collection_slug>/',
          views.product_list_by_collection,
            name='product_list_by_collection'),
    path('<slug:category_slug>/',
          views.product_list,
            name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',
          views.product_detail,
            name='product_detail'),
]