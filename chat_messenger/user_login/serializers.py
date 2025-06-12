# users/serializers.py

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'profile_picture', 'security_question', 'security_answer']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            profile_picture=validated_data.get('profile_picture'),
            security_question=validated_data.get('security_question'),
            security_answer=validated_data.get('security_answer'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
