from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .serializers import LecturerSerializer
from . import models

class LecturerList(generics.ListCreateAPIView):
    queryset = models.Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [permissions.IsAuthenticated]

class LecturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes=[permissions.IsAuthenticated]