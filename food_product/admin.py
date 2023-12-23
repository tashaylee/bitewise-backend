from django.contrib import admin
from food_product.models import FoodProduct


class FoodProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FoodProduct._meta.get_fields()]


admin.site.register(FoodProduct, FoodProductAdmin)