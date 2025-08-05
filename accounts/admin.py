from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    
    
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('email', 'phone_number')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    
    
    list_display = ('user', 'location', )
    search_fields = ('user__email', 'user__username', 'location',)
    list_filter = ('location',)
