from django.contrib import admin
from shared.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone')


admin.site.register(User, UserAdmin)
