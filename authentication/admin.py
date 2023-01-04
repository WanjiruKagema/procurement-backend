from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from authentication.models import User


class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff',
                    'is_procurement_officer', 'is_head_department', 'is_procurement_committee', 'is_head_of_finance',
                    'is_ceo')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'groups',
                           'user_permissions',)}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'department')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_procurement_officer', 'is_head_department',
                                    'is_procurement_committee', 'is_head_of_finance', 'is_ceo')}),

    )


admin.site.register(User, UserAdmin)
