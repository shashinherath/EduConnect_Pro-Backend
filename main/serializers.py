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
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('admin', None)
        if user_data is not None:
            user = instance.admin
            for key, value in user_data.items():
                if key == 'username' and user.username == value:
                    continue  # Skip updating the username if it's the same
                setattr(user, key, value)
            user.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    


class LecturerSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = models.Lecturer
        fields = ['id', 'admin', 'profile_pic', 'phone_number', 'role', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('admin')
        user, user_created = models.CustomUser.objects.get_or_create(**user_data)
        if not user_created:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
        lecturer, created = models.Lecturer.objects.update_or_create(admin=user, defaults=validated_data)
        return lecturer
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('admin', None)
        if user_data is not None:
            user = instance.admin
            for key, value in user_data.items():
                if key == 'username' and user.username == value:
                    continue
                setattr(user, key, value)
            user.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



class StudentSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = models.Student
        fields = ['id', 'admin', 'profile_pic', 'level', 'phone_number', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('admin')
        user, user_created = models.CustomUser.objects.get_or_create(**user_data)
        if not user_created:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
        student, created = models.Student.objects.update_or_create(admin=user, defaults=validated_data)
        return student
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('admin', None)
        if user_data is not None:
            user = instance.admin
            for key, value in user_data.items():
                if key == 'username' and user.username == value:
                    continue
                setattr(user, key, value)
            user.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    

#create course serializer here
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name', 'image', 'description', 'created_at', 'updated_at']

        def create(self, validated_data):
            course = models.Course.objects.create(**validated_data)
            return course
        
        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        

