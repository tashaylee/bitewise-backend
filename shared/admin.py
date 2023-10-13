from django.contrib import admin
from shared.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget', 'first_name', 'last_name', 'email')


admin.site.register(User, UserAdmin)
