from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'user_type']

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
        # Check if the user already exists
        user, user_created = models.CustomUser.objects.get_or_create(**user_data)
        if not user_created:
            # If the user already exists, update the user with the new data
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
        # Now, proceed with creating or updating the Admin instance
        admin, created = models.Admin.objects.update_or_create(admin=user, defaults=validated_data)
        return admin


