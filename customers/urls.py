from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('customer/autocomplete', views.customer_autocomplete, name='customer-autocomplete'),

    path("customer/list/", views.CustomerListView.as_view(), name='customer-list'),
    path("customer/add/", views.CustomerCreateView.as_view(), name='customer-create'),
    path("customer/<int:pk>/edit/", views.CustomerUpdateView.as_view(), name='customer-update'),
    path("customer/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name='customer-delete'),

    path("address/list/", views.CustomerAddressList.as_view(), name='address-list'),
    path("address/add/", views.CustomerAddressCreate.as_view(), name='address-create'),
    path("address/<int:pk>/edit/", views.CustomerAddressUpdate.as_view(), name='address-update'),
    path("address/<int:pk>/delete/", views.CustomerAddressDelete.as_view(), name='address-delete'),
]
