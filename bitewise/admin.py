from django.contrib import admin
from .models import *

class CommitmentCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'year', 'month', 'week', 'count')

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'monthlyAmount', 'groceryAmount', 'otherAmount')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget', 'first_name', 'last_name', 'email')

# Register your models here.

admin.site.register(CommitmentCount, CommitmentCountAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(User, UserAdmin)