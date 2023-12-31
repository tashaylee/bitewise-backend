from rest_framework import serializers
from shared.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone')

    def create(self, validated_data):
        # Combine first_name and last_name to create username
        username = f"{validated_data['first_name']}_{validated_data['last_name']}"
        validated_data['username'] = username

        # Convert PhoneNumber to string
        phone_number = validated_data.get('phone')
        if phone_number:
            validated_data['phone'] = str(phone_number)
        return super().create(validated_data)
