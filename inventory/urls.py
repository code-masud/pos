from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('brand', views.BrandList.as_view(), name='brand'),
    path('brand/add/', views.BrandAdd.as_view(), name='brand-add'),
    path('brand/<int:pk>/edit/', views.BrandUpdate.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', views.BrandDelete.as_view(), name='brand-delete'),

    path('category', views.CategoryList.as_view(), name='category'),
    path('category/add/', views.CategoryAdd.as_view(), name='category-add'),
    path('category/<int:pk>/edit/', views.CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category-delete'),

    path('product', views.ProductList.as_view(), name='product'),
    path('product/add/', views.ProductAdd.as_view(), name='product-add'),
    path('product/<int:pk>/edit/', views.ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product-delete'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api-products'),

    path('stock', views.StockList.as_view(), name='stock'),
    path('stock/add/', views.StockAdd.as_view(), name='stock-add'),
    path('stock/<int:pk>/edit/', views.StockUpdate.as_view(), name='stock-update'),
    path('stock/<int:pk>/delete/', views.StockDelete.as_view(), name='stock-delete'),

    path('movement', views.StockMovementList.as_view(), name='movement'),
    path('movement/add/', views.StockMovementAdd.as_view(), name='movement-add'),
    path('movement/<int:pk>/edit/', views.StockMovementUpdate.as_view(), name='movement-update'),
    path('movement/<int:pk>/delete/', views.StockMovementDelete.as_view(), name='movement-delete'),
]
