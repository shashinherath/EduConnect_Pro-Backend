from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(**validated_data)
        return user

class AdminSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = models.Admin
        fields = ['id', 'admin', 'profile_pic', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('admin')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        admin, created = models.Admin.objects.update_or_create(admin=user, **validated_data)
        return admin


