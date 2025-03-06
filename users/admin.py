from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email','first_name', 'last_name', 'sex', 'user_type','date_join', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name','sex', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
     
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email','first_name', 'user_type','last_name','sex', 'date_join')
    search_fields = ('user__username', 'email')
    list_filter = ('date_join',)

admin.site.register(Profile, ProfileAdmin)
