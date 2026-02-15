from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/', views.PointsOfSale.as_view(), name='pos'),
    path('cart/add/', views.add_to_cart, name='cart-add'),
    path('cart/<int:id>/delete/', views.cart_delete, name='cart-delete'),
    path('cart/<int:id>/increment/', views.cart_increment, name='cart-increment'),
    path('cart/<int:id>/decrement/', views.cart_decrement, name='cart-decrement'),

    path('sale/', views.SaleList.as_view(), name='sale-list'),
    path('sale/add/', views.SaleAdd.as_view(), name='sale-add'),
    path('sale/<int:pk>/edit/', views.SaleUpdate.as_view(), name='sale-update'),
    path('sale/<int:pk>/delete/', views.SaleDelete.as_view(), name='sale-delete'),

    path('saleitem/', views.SaleItemList.as_view(), name='saleitem-list'),
    path('saleitem/add/', views.SaleItemAdd.as_view(), name='saleitem-add'),
    path('saleitem/<int:pk>/edit/', views.SaleItemUpdate.as_view(), name='saleitem-update'),
    path('saleitem/<int:pk>/delete/', views.SaleItemDelete.as_view(), name='saleitem-delete'),
]
