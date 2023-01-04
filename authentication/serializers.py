from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

        def create(self, validated_data):
            email = validated_data['email']
            password = validated_data['password']

            user = User.objects.create_user(
                email=email,
                password=password
            )

            return user


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name']
