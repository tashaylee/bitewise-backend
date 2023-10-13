from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('user_id', 'monthlyAmount', 'groceryAmount', 'otherAmount')
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data, *args, **kwargs):
        monthly_budget = validated_data.get('monthlyAmount', None)
        grocery_percentage = validated_data.get('groceryAmount', None)

        # Calculate 'otherAmount' and 'groceryAmount' based on the provided 'monthlyAmount' and 'groceryAmount'
        other_percentage = 100 - grocery_percentage
        validated_data['groceryAmount'] = monthly_budget * (grocery_percentage / 100)
        validated_data['otherAmount'] = monthly_budget * (other_percentage / 100)

        budget, created = Budget.objects.update_or_create(defaults={**validated_data})
        return budget
