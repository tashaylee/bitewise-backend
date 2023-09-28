from rest_framework import serializers
from .models import *

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'user', 'monthlyAmount', 'groceryAmount', 'otherAmount')

class CommitmentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitmentCount
        fields = ('id', 'user', 'year', 'month', 'week', 'count')
        read_only_fields = ('user',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'budget', 'first_name', 'last_name', 'email')
        read_only_fields = ('budget',)
