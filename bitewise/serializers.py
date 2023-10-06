from rest_framework import serializers
from .models import *
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'budget', 'first_name', 'last_name', 'email')
        read_only_fields = ('budget',)

class CommitmentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitmentCount
        fields = ('id', 'user', 'year', 'month', 'week', 'count', 'created_at')
        extra_kwargs = {'user': {'read_only': True}}
    
    def create(self, validated_data, *args, **kwargs):
        commitment_count = CommitmentCount.objects.create(**validated_data)
        return commitment_count
    
class MealCommitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCommitment
        fields = '__all__'
        read_only_fields = ('commitment_count',)
    

class BudgetSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id')
    otherAmount = serializers.SerializerMethodField('calculate_other')

    class Meta:
        model = Budget
        fields = ('user_id', 'monthlyAmount', 'groceryAmount', 'otherAmount')
        extra_kwargs = {'user': {'read_only': True}}
    
    def calculate_other(self, instance):
        return 100 - instance.groceryAmount

    def create(self, validated_data, *args, **kwargs):
        user = validated_data.pop('user')
        budget, created = Budget.objects.update_or_create(user=user, defaults={**validated_data})
        return budget