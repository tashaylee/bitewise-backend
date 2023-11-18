from django.contrib import admin
from ingredients.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Ingredient._meta.get_fields()]


admin.site.register(Ingredient, IngredientAdmin)
