from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    otherAmount = serializers.SerializerMethodField('calculate_other')

    class Meta:
        model = Budget
        fields = ('user_id', 'monthlyAmount', 'groceryAmount', 'otherAmount')
        extra_kwargs = {'user': {'read_only': True}}

    def calculate_other(self, instance):
        return 100 - instance.groceryAmount

    def create(self, validated_data, *args, **kwargs):
        user = validated_data.pop('user')
        budget, created = Budget.objects.update_or_create(
            user=user, defaults={**validated_data})
        return budget
