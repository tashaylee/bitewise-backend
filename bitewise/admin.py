from django.contrib import admin
from .models import *

class CommitmentCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'year', 'month', 'week', 'count', 'created_at')


class MealCommitmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'achieved', 'activated', 'commitment_count')

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'monthlyAmount', 'groceryAmount', 'otherAmount')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget', 'first_name', 'last_name', 'email')

# Register your models here.

admin.site.register(CommitmentCount, CommitmentCountAdmin)
admin.site.register(MealCommitment, MealCommitmentAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(User, UserAdmin)