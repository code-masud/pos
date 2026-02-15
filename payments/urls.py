from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment/', views.PaymentList.as_view(), name='payment-list'),
    path('payment/add/', views.PaymentCreate.as_view(), name='payment-create'),
    path('payment/<int:pk>/edit/', views.PaymentUpdate.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete/', views.PaymentDelete.as_view(), name='payment-delete'),

    path('refund/', views.RefundList.as_view(), name='refund-list'),
    path('refund/add/', views.RefundCreate.as_view(), name='refund-create'),
    path('refund/<int:pk>/edit/', views.RefundUpdate.as_view(), name='refund-update'),
    path('refund/<int:pk>/delete/', views.RefundDelete.as_view(), name='refund-delete'),

    path('payment-method/', views.PaymentMethodList.as_view(), name='payment-method-list'),
    path('payment-method/add/', views.PaymentMethodCreate.as_view(), name='payment-method-create'),
    path('payment-method/<int:pk>/edit/', views.PaymentMethodUpdate.as_view(), name='payment-method-update'),
    path('payment-method/<int:pk>/delete/', views.PaymentMethodDelete.as_view(), name='payment-method-delete'),
]
