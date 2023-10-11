from rest_framework import serializers
from .models import *


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
