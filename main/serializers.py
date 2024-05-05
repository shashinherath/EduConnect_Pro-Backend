from rest_framework import serializers
from . import models

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lecturer
        fields = '__all__'