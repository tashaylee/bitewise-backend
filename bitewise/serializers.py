from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'budget', 'first_name', 'last_name', 'email')
        read_only_fields = ('budget',)

class CommitmentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitmentCount
        fields = ('id', 'user', 'year', 'month', 'week', 'count')
        read_only_fields = ('user',)

class BudgetSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id')
    class Meta:
        model = Budget
        fields = ('user_id', 'monthlyAmount', 'groceryAmount', 'otherAmount')
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data, *args, **kwargs):
        user_id = validated_data.pop('user')
        budget, created = Budget.objects.update_or_create(user__id=user_id, defaults={**validated_data})
        return budget