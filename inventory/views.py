from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Brand, Category, Product, Stock, StockMovement
from .forms import BrandForm, CategoryForm, ProductForm, StockForm, StockMovementForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from .services import apply_stock_movement

class ProductPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 100

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'sku', 'description', 'category__name', 'brand__name']

class BrandList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Brand
    template_name = 'inventory/brand/brand_list.html'
    form_class = BrandForm
    permission_required = ['inventory:view_brand']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Brand List'
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

class BrandAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Brand
    template_name = 'inventory/brand/partials/brand_form.html'
    form_class = BrandForm
    row_template = 'inventory/brand/partials/brand_row.html'
    context_object_name = 'brand'
    success_url = reverse_lazy('inventory:brand')
    permission_required = ['inventory:add_brand']
    htmx_trigger = 'closeModal'

class BrandUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Brand
    template_name = 'inventory/brand/partials/brand_form.html'
    form_class = BrandForm
    row_template = 'inventory/brand/partials/brand_row.html'
    context_object_name = 'brand'
    success_url = reverse_lazy('inventory:brand')
    permission_required = ['inventory:change_brand']

class BrandDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Brand
    template_name = 'inventory/brand/partials/brand_confirm_delete.html'
    form_class = BrandForm
    success_url = reverse_lazy('inventory:brand')
    permission_required = ['inventory:delete_brand']
    
class CategoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category/category_list.html'
    form_class = CategoryForm
    permission_required = ['inventory:view_category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Category List'
        return context

class CategoryAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'inventory/category/partials/category_form.html'
    form_class = CategoryForm
    row_template = 'inventory/category/partials/category_row.html'
    context_object_name = 'category'
    success_url = reverse_lazy('inventory:category')
    permission_required = ['inventory:add_category']
    htmx_trigger = 'closeModal'

class CategoryUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'inventory/category/partials/category_form.html'
    form_class = CategoryForm
    row_template = 'inventory/category/partials/category_row.html'
    context_object_name = 'category'
    success_url = reverse_lazy('inventory:category')
    permission_required = ['inventory:change_category']

class CategoryDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category/partials/category_confirm_delete.html'
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category')
    permission_required = ['inventory:delete_category']
    
class ProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product/product_list.html'
    form_class = ProductForm
    permission_required = ['inventory:view_product']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Product List'
        return context

class ProductAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/product/partials/product_form.html'
    form_class = ProductForm
    row_template = 'inventory/product/partials/product_row.html'
    context_object_name = 'product'
    success_url = reverse_lazy('inventory:product')
    permission_required = ['inventory:add_product']
    htmx_trigger = 'closeModal'

class ProductUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'inventory/product/partials/product_form.html'
    form_class = ProductForm
    row_template = 'inventory/product/partials/product_row.html'
    context_object_name = 'product'
    success_url = reverse_lazy('inventory:product')
    permission_required = ['inventory:change_product']

class ProductDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product/partials/product_confirm_delete.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:product')
    permission_required = ['inventory:delete_product']

class StockList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Stock
    template_name = 'inventory/stock/stock_list.html'
    form_class = StockForm
    permission_required = ['inventory:view_stock']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Stock List'
        return context
    
class StockAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Stock
    template_name = 'inventory/stock/partials/stock_form.html'
    form_class = StockForm
    row_template = 'inventory/stock/partials/stock_row.html'
    context_object_name = 'stock'
    success_url = reverse_lazy('inventory:stock')
    permission_required = ['inventory:add_stock']
    htmx_trigger = 'closeModal'

class StockUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Stock
    template_name = 'inventory/stock/partials/stock_form.html'
    form_class = StockForm
    row_template = 'inventory/stock/partials/stock_row.html'
    context_object_name = 'stock'
    success_url = reverse_lazy('inventory:stock')
    permission_required = ['inventory:change_stock']

class StockDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Stock
    template_name = 'inventory/stock/partials/stock_confirm_delete.html'
    form_class = StockForm
    success_url = reverse_lazy('inventory:stock')
    permission_required = ['inventory:delete_stock']
    
class StockMovementList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/movement/movement_list.html'
    form_class = StockMovementForm
    permission_required = ['inventory:view_stock_movement']
    context_object_name = 'stock_movement_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Movement List'
        return context
    
class StockMovementAdd(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = StockMovement
    template_name = 'inventory/movement/partials/movement_form.html'
    form_class = StockMovementForm
    row_template = 'inventory/movement/partials/movement_row.html'
    context_object_name = 'stock_movement'
    success_url = reverse_lazy('inventory:movement')
    permission_required = ['inventory:add_stock_movement']
    htmx_trigger = 'closeModal'

    def form_valid(self, form):
        movement = form.save()
        apply_stock_movement(movement=movement, user=self.request.user)
        return super().form_valid(form)
    

class StockMovementUpdate(HtmxFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = StockMovement
    template_name = 'inventory/movement/partials/movement_form.html'
    form_class = StockMovementForm
    row_template = 'inventory/movement/partials/movement_row.html'
    context_object_name = 'stock_movement'
    success_url = reverse_lazy('inventory:movement')
    permission_required = ['inventory:change_stock_movement']

class StockMovementDelete(HtmxPostMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = StockMovement
    template_name = 'inventory/movement/partials/movement_confirm_delete.html'
    form_class = StockMovementForm
    success_url = reverse_lazy('inventory:movement')
    permission_required = ['inventory:delete_stock_movement']