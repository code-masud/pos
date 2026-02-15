from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = 'accounts'

urlpatterns = [
    path("company/", views.CompanyView.as_view(), name='company'),
    path("profile/<int:pk>/", views.AccountsProfile.as_view(), name='user-profile'),
    path("user/list/", views.UserListView.as_view(), name='user-list'),
    path("user/add/", views.UserCreateView.as_view(), name='user-create'),
    path("user/<int:pk>/edit/", views.UserUpdateView.as_view(), name='user-update'),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name='user-delete'),

    path("branch/list/", views.BranchListView.as_view(), name='branch-list'),
    path("branch/add/", views.BranchCreateView.as_view(), name='branch-create'),
    path("branch/<int:pk>/edit/", views.BranchUpdateView.as_view(), name='branch-update'),
    path("branch/<int:pk>/delete/", views.BranchDeleteView.as_view(), name='branch-delete'),
]
