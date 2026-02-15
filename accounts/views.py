import sweetify
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView, FormView
from .forms import CustomUserCreationForm, CustomUserChangeForm, CompanyForm
from .models import Branch, Company

User = get_user_model()

class CompanyView(FormView):
    template_name = "accounts/company.html"
    form_class = CompanyForm
    success_url = reverse_lazy("accounts:company")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = Company.objects.first()
        return kwargs

    def form_valid(self, form):
        form.save()
        sweetify.success(self.request, "Company updated successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Company"
        return context
    
class AccountsProfile(DetailView):
    model = User
    template_name = 'accounts/user/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Profile'
        return context
    
class UserListView(ListView):
    model = User
    template_name = 'accounts/user/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'User List'
        return context
    
class UserCreateView(CreateView):
    model = User
    template_name = 'accounts/user/user_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'User Create'
        return context
    
    def form_valid(self, form):
        sweetify.success(self.request, f'User created successfully')
        return super().form_valid(form)
    
    
class UserUpdateView(UpdateView):
    model = User
    template_name = 'accounts/user/user_form.html'
    form_class = CustomUserChangeForm
    
    def get_success_url(self):
        sweetify.success(self.request, f'User updated successfully')
        return reverse_lazy('accounts:user-profile', kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'User Update'
        return context
    
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        sweetify.success(self.request, f'User deleted successfully')
        return super().post(request, *args, **kwargs)
    
class BranchListView(ListView):
    model = Branch
    template_name = 'accounts/branch/branch_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Branch List'
        return context

class BranchCreateView(CreateView):
    model = Branch
    fields = ["name", "code", 'phone', 'email', 'address']
    template_name = "accounts/branch/partials/branch_form.html"
    success_url = reverse_lazy("accounts:branch-list")

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('HX-Request'):
            response = render(
                self.request,
                'accounts/branch/partials/branch_row.html',
                {"branch": self.object}
            )
            response['HX-Trigger'] = 'closeModal'
            return response
        return super().form_valid(form)


class BranchUpdateView(UpdateView):
    model = Branch
    fields = ["name", "code", 'phone', 'email', 'address']
    template_name = "accounts/branch/partials/branch_form.html"
    success_url = reverse_lazy("accounts:branch-list")
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('HX-Request'):
            response = render(
                self.request,
                'accounts/branch/partials/branch_row.html',
                {"branch": self.object}
            )
            response['HX-Trigger'] = 'closeModal'
            return response
        return super().form_valid(form)

class BranchDeleteView(DeleteView):
    model = Branch
    template_name = "accounts/branch/partials/branch_confirm_delete.html"
    success_url = reverse_lazy("accounts:branch-list")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        if request.headers.get("HX-Request"):
            response = HttpResponse("")
            response["HX-Trigger"] = "closeModal"
            return response

        return super().post(request, *args, **kwargs)