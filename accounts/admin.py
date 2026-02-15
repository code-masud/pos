from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Company
from django.utils.html import format_html

User = get_user_model()

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = ['name', 'logo_preview', 'phone', 'email', 'address']
    list_display_links = ['name', 'logo_preview', 'phone', 'email']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src={} style="width:100px; height:50px;">',
                obj.logo.url
            )
        return '--'
    logo_preview.short_description = 'Logo'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Forms
    form = UserChangeForm
    add_form = UserCreationForm

    # List view configuration
    list_display = (
        'id',
        'username',
        'avatar',
        'phone',
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('id', 'username')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('username', 'phone', 'email')
    ordering = ('username',)
    list_per_page = 10
    list_select_related = ()  # Add related fields here if needed

    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')

    # Many-to-many fields
    filter_horizontal = ('branches', 'groups', 'user_permissions')

    def avatar(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height=50px">',
                obj.image.url
            )
        return '--'
    avatar.short_description = 'Image'
    # Add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'phone',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )

    # Edit user page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'email',
                'image',
                'address',
                'role',
                'branches',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login')
        }),
    )


