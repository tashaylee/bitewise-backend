from rest_framework import serializers
from food_product.models import FoodProduct


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = '__all__'
