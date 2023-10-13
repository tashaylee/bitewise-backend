from django.contrib import admin
from budget.models import Budget


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'monthlyAmount', 'groceryAmount', 'otherAmount')

admin.site.register(Budget, BudgetAdmin)