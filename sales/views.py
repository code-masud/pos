from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from inventory.models import Product
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from payments.models import PaymentMethod
import sweetify
from .services import create_sale
from django.urls import reverse_lazy

class InvoiceView(DetailView):
    model = Sale
    template_name = 'sales/sale/invoice.html'

    def get_context_data(self, **kwargs):
        sale = self.get_object()
        context = super().get_context_data(**kwargs)
        context["title"] = f'Invoice #{sale.id}'
        return context

class PointsOfSale(LoginRequiredMixin, TemplateView):
    template_name = 'sales/pos/pos.html'

    def post(self, request):
        try:
            cart = request.session.get("cart")
            post = request.POST

            sale = create_sale(cart_data=cart, post_data=post, user=request.user)

            request.session.pop("cart", None)
            request.session.modified = True

            sweetify.success(request, f'Sale #{sale.id} created successfully.', timer="3000")
            return redirect("sales:invoice", pk=sale.id)
        except Exception as e:
            sweetify.error(request, str(e), timer="3000")
            
        return redirect("sales:pos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart.cart
        context['total'] = cart.total
        context['total_qty'] = cart.total_qty
        context['payment_methods'] = PaymentMethod.objects.all().order_by('id')
        context["title"] = 'Points Of Sale'
        return context
    
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity", "0")
        price = request.POST.get("price", "0")
        tax_rate = request.POST.get("tax_rate", "0")
        apply_tax = request.POST.get("apply_tax") == "on"

        product_obj = get_object_or_404(Product, pk=product_id)

        # Convert safely to Decimal
        try:
            price = Decimal(price)
            quantity = Decimal(quantity)
            tax_rate = Decimal(tax_rate)
        except:
            return JsonResponse({"error": "Invalid numeric values"}, status=400)

        if quantity <= 0:
            return JsonResponse({"error": "Quantity must be greater than zero"}, status=400)

        # Apply tax (tax-exclusive model)
        if not apply_tax:
            tax_rate = Decimal("0.00")

        cart = Cart(request)

        cart_item = {
            "id": str(product_obj.id),
            "name": product_obj.name,
            "price": str(price),
            "qty": str(quantity),
            "tax_rate": str(tax_rate),
        }

        cart.add(**cart_item)

        return render(request, "sales/pos/cart/cart.html", {
            "cart": cart.cart,
            "total": cart.total(),
            "total_qty": cart.total_qty(),
        })
    cart = request.session.get("cart", {})
    return render(request, 'sales/pos/cart/cart.html', {"cart": cart})

def cart_delete(request, id):
    cart = Cart(request)
    cart.remove(product_id=id)
    
    return render(request, "sales/pos/cart/cart.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "total_qty": cart.total_qty(),
    })

def cart_increment(request, id):
    cart = Cart(request)
    cart.increment(product_id=id)

    return render(request, "sales/pos/cart/cart.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "total_qty": cart.total_qty(),
    })


def cart_decrement(request, id):
    cart = Cart(request)
    cart.decrement(product_id=id)

    return render(request, "sales/pos/cart/cart.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "total_qty": cart.total_qty(),
    })

class SaleList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale/sale_list.html'
    permission_required = ['sales:view_sale']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sale List"
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
    
class SaleAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Sale
    template_name = 'sales/sale/partials/sale_form.html'
    form_class = SaleForm
    row_template = 'sales/sale/partials/sale_row.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:add_sale']
    htmx_trigger = 'closeModal'

class SaleUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Sale
    template_name = 'sales/sale/partials/sale_form.html'
    form_class = SaleForm
    row_template = 'sales/sale/partials/sale_row.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:change_sale']

class SaleDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sales/sale/partials/sale_confirm_delete.html'
    form_class = SaleForm
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:delete_sale']

class SaleItemList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SaleItem
    form_class = SaleItemForm
    template_name = 'sales/saleitem/saleitem_list.html'
    permission_required = ['sales:view_sale_item']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "SaleItem List"
        return context
    
class SaleItemAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SaleItem
    template_name = 'sales/saleitem/partials/saleitem_form.html'
    form_class = SaleItemForm
    row_template = 'sales/saleitem/partials/saleitem_row.html'
    context_object_name = 'saleitem'
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:add_sale_item']
    htmx_trigger = 'closeModal'

class SaleItemUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SaleItem
    template_name = 'sales/saleitem/partials/saleitem_form.html'
    form_class = SaleItemForm
    row_template = 'sales/saleitem/partials/saleitem_row.html'
    context_object_name = 'saleitem'
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:change_sale_item']

class SaleItemDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SaleItem
    template_name = 'sales/saleitem/partials/saleitem_confirm_delete.html'
    form_class = SaleItemForm
    success_url = reverse_lazy('sales:sale')
    permission_required = ['sales:delete_sale_item']
