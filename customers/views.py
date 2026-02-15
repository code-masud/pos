from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import CustomerSerializer
from .models import Customer, CustomerAddress
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import CustomerForm, CustomerAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

# Create your views here.
def customer_autocomplete(request):
    query = request.GET.get('q', None)

    customers = []
    if query:
        customers = Customer.objects.filter(Q(name__icontains=query)|Q(phone__icontains=query)|Q(email__icontains=query)|Q(addresses__address__icontains=query))[:10]
    else: customers = Customer.objects.all()
    
    return render(request, 'customers/customer/partials/customer_autocomplete.html', {'customers': customers})

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Customer List'
        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer/partials/customer_form.html"
    success_url = reverse_lazy("customers:customer-list")

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('HX-Request'):
            response = render(
                self.request,
                'customers/customer/partials/customer_row.html',
                {"customer": self.object}
            )
            response['HX-Trigger'] = 'closeModal'
            return response
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer/partials/customer_form.html"
    success_url = reverse_lazy("customers:customer-list")
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('HX-Request'):
            response = render(
                self.request,
                'customers/customer/partials/customer_row.html',
                {"customer": self.object}
            )
            response['HX-Trigger'] = 'closeModal'
            return response
        return super().form_valid(form)

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "customers/customer/partials/customer_confirm_delete.html"
    success_url = reverse_lazy("customers:customer-list")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        if request.headers.get("HX-Request"):
            response = HttpResponse("")
            response["HX-Trigger"] = "closeModal"
            return response

        return super().post(request, *args, **kwargs)
    
class CustomerAddressList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomerAddress
    template_name = 'customers/customer_address/customer_address_list.html'
    form_class = CustomerAddressForm
    permission_required = ['customers:view_customer_address']
    context_object_name = 'customer_address_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'CustomerAddress List'
        return context

class HtmxFormMixin:
    row_template = None
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            response = render(self.request, self.row_template, {self.context_object_name: self.object})
            response['HX-Trigger'] = self.htmx_trigger
            return response
        
        return super().form_valid(form)
    
class HtmxPostMixin:
    row_template = None
    htmx_trigger = 'closeModal'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if self.request.headers.get('HX-Request'):
            response = HttpResponse("")
            response['HX-Trigger'] = self.htmx_trigger
            return response
        
        return super().post(request, *args, **kwargs)

class CustomerAddressCreate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerAddress
    template_name = 'customers/customer_address/partials/customer_address_form.html'
    form_class = CustomerAddressForm
    row_template = 'customers/customer_address/partials/customer_address_row.html'
    context_object_name = 'address'
    success_url = reverse_lazy('customers:customer_address')
    permission_required = ['customers:add_customer_address']
    htmx_trigger = 'closeModal'

class CustomerAddressUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerAddress
    template_name = 'customers/customer_address/partials/customer_address_form.html'
    form_class = CustomerAddressForm
    row_template = 'customers/customer_address/partials/customer_address_row.html'
    context_object_name = 'address'
    success_url = reverse_lazy('customers:customer_address')
    permission_required = ['customers:change_customer_address']

class CustomerAddressDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerAddress
    template_name = 'customers/customer_address/partials/customer_address_confirm_delete.html'
    form_class = CustomerAddressForm
    success_url = reverse_lazy('customers:customer_address')
    permission_required = ['customers:delete_customer_address']