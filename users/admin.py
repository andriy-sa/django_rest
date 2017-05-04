from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AppUserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (('Personal info'), {'fields': ('username',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, AppUserAdmin)
