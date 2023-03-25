from rest_framework import serializers
from .models import Password, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if User.objects.filter(email=data["email"]):
            raise serializers.ValidationError({"email": "already used"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ["id", "user",
                  "password",
                  "title",
                  "website",
                  "algo",
                  "iterations", "salt"]
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response
