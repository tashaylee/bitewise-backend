from rest_framework import serializers
from shared.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'budget', 'first_name', 'last_name', 'email')
        read_only_fields = ('budget',)
