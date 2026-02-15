from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Payment, PaymentMethod, Refund
from .forms import PaymentForm, PaymentMethodForm, RefundForm
from django.db import transaction
from django.core.exceptions import ValidationError
import sweetify

class PaymentMethodList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PaymentMethod
    template_name = 'payments/payment_method/payment_method_list.html'
    context_object_name = 'payment_method_list'
    permission_required = ['payments:view_payment_method']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Payment Method List'
        return context
    
class FormMixin:
    template_row = None
    hx_trigger = 'closeModal'

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('HX-Request'):
            response = render(self.request, self.template_row, {self.context_object_name:self.object})
            response['HX-Trigger'] = self.hx_trigger
            return response
        return super().form_valid(form)
    
class PostMixin:
    template_row = None
    hx_trigger = 'closeModal'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if self.request.headers.get('HX-Request'):
            response = HttpResponse("")
            response['HX-Trigger'] = self.hx_trigger
            return response
        return super(request, *args, **kwargs)
    
class PaymentMethodCreate(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'payments/payment_method/partials/payment_method_form.html'
    context_object_name = 'payment_method'
    permission_required = ['payments:add_payment_method']
    success_url = reverse_lazy('payments:payment-method-list')
    template_row = 'payments/payment_method/partials/payment_method_row.html'

class PaymentMethodUpdate(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'payments/payment_method/partials/payment_method_form.html'
    context_object_name = 'payment_method'
    permission_required = ['payments:change_payment_method']
    success_url = reverse_lazy('payments:payment-method-list')
    template_row = 'payments/payment_method/partials/payment_method_row.html'
    
class PaymentMethodDelete(LoginRequiredMixin, PermissionRequiredMixin, PostMixin, DeleteView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'payments/payment_method/partials/payment_method_confirm_delete.html'
    context_object_name = 'payment_method'
    permission_required = ['payments:delete_payment_method']
    success_url = reverse_lazy('payments:payment-method-list')

class PaymentList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment/payment_list.html'
    permission_required = ['payments:view_payment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Payment List'
        return context
    
class PaymentCreate(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment/partials/payment_form.html'
    context_object_name = 'payment'
    permission_required = ['payments:add_payment']
    success_url = reverse_lazy('payments:payment-method-list')
    template_row = 'payments/payment/partials/payment_row.html'

class PaymentUpdate(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment/partials/payment_form.html'
    context_object_name = 'payment'
    permission_required = ['payments:change_payment']
    success_url = reverse_lazy('payments:payment-method-list')
    template_row = 'payments/payment/partials/payment_row.html'
    
class PaymentDelete(LoginRequiredMixin, PermissionRequiredMixin, PostMixin, DeleteView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment/partials/payment_confirm_delete.html'
    context_object_name = 'payment'
    permission_required = ['payments:delete_payment']
    success_url = reverse_lazy('payments:payment-method-list')

class RefundList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Refund
    template_name = 'payments/refund/refund_list.html'
    permission_required = ['payments:view_payment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Refund List'
        return context

class RefundCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Refund
    form_class = RefundForm
    template_name = 'payments/refund/partials/refund_form.html'
    context_object_name = 'refund'
    permission_required = ['payments.add_refund']
    success_url = reverse_lazy('payments:refund-list')

    def form_valid(self, form):
        refund = form.instance
        payment = refund.payment
        
        with transaction.atomic():

            # Validate payment status
            if payment.status != "completed":
                form.add_error(None, "Only completed payments can be refunded.")
                return self.form_invalid(form)

            # Validate refund amount
            if refund.amount > payment.refundable_amount():
                form.add_error("amount", "Refund exceeds available balance.")
                return self.form_invalid(form)

            refund.sale = payment.sale
            # refund.processed_by = self.request.user
            # refund.status = "completed"

            response = super().form_valid(form)

            # Update payment status
            if payment.refundable_amount() == 0:
                payment.status = "refunded"
                payment.save()

            return response
        
class RefundUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Refund
    form_class = RefundForm
    template_name = 'payments/refund/partials/refund_form.html'
    context_object_name = 'refund'
    permission_required = ['payments.change_refund']
    success_url = reverse_lazy('payments:refund-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == "completed":
            sweetify.error(request, "Completed refunds cannot be edited.")
            return redirect('payments:refund-list')
            raise ValidationError("Completed refunds cannot be edited.")
        return super().dispatch(request, *args, **kwargs)

    
class RefundDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Refund
    template_name = 'payments/refund/partials/refund_confirm_delete.html'
    context_object_name = 'refund'
    permission_required = ['payments.delete_refund']
    success_url = reverse_lazy('payments:refund-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == "completed":
            sweetify.error(request, "Completed refunds cannot be deleted.")
            return redirect('payments:refund-list')
            raise ValidationError("Completed refunds cannot be deleted.")
        return super().dispatch(request, *args, **kwargs)
