from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Admin, Lecturer, Course, Student, Chat, Attendence, LectureMaterial
from .serializers import AdminSerializer, LecturerSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, parser_classes
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser

#Create your views here.

@api_view(['POST'])
def doLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_type': user.user_type}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def doLogout(request):
    request.user.auth_token.delete()
    return Response({'success': 'Logout successfully'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def admin_add(request):
    if request.method == 'POST':
        user_data = {}

        if 'username' in request.data:
            user_data['username'] = request.data['username']
        if 'first_name' in request.data:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data:
            user_data['email'] = request.data['email']
        if 'password' in request.data:
            user_data['password'] = request.data['password']
        if 'user_type' in request.data:
            user_data['user_type'] = request.data['user_type']

        admin_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            admin_data["profile_pic"] = request.data.get("profile_pic")


        admin_serializer = AdminSerializer(data=admin_data, partial=True)
        if admin_serializer.is_valid():
            admin_serializer.save()
            return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
        return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_api(request):
    if request.method == 'GET':
        admins = Admin.objects.all()
        admin_serializer = AdminSerializer(admins, many=True)
        return Response(admin_serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_detail(request, pk):
    try:
        admin = Admin.objects.get(pk=pk)
    except Admin.DoesNotExist:
        return Response({'error': 'Admin does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        admin_serializer = AdminSerializer(admin)
        return Response(admin_serializer.data)

    elif request.method == 'PUT':
        user_data = {}
        
        if 'username' in request.data and request.data['username'] != admin.admin.username:
            user_data['username'] = request.data['username']
        if 'first_name' in request.data and request.data['first_name'] != admin.admin.first_name:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data and request.data['last_name'] != admin.admin.last_name:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data and request.data['email'] != admin.admin.email:
            user_data['email'] = request.data['email']
        if 'password' in request.data and request.data['password'] != admin.admin.password:
            user_data['password'] = request.data['password']
        if 'user_type' in request.data and request.data['user_type'] != admin.admin.user_type:
            user_data['user_type'] = request.data['user_type']

        admin_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            admin_data["profile_pic"] = request.data.get("profile_pic")

        admin_serializer = AdminSerializer(admin, data=admin_data, partial=True)
        if admin_serializer.is_valid():
            admin_serializer.save()
            return Response(admin_serializer.data)
        return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user = CustomUser.objects.get(username=admin.admin.username)
        user.delete()
        admin.delete()
        return Response({'success': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

#create lecturer_add api here
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def lecturer_add(request):
    if request.method == 'POST':
        user_data = {}

        if 'username' in request.data:
            user_data['username'] = request.data['username']
        if 'first_name' in request.data:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data:
            user_data['email'] = request.data['email']
        if 'password' in request.data:
            user_data['password'] = request.data['password']
        if 'user_type' in request.data:
            user_data['user_type'] = request.data['user_type']

        lecturer_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            lecturer_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("phone_number"):
            lecturer_data["phone_number"] = request.data.get("phone_number")
        if request.data.get("role"):
            lecturer_data["role"] = request.data.get("role")

        lecturer_serializer = LecturerSerializer(data=lecturer_data, partial=True)
        if lecturer_serializer.is_valid():
            lecturer_serializer.save()
            return Response(lecturer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(lecturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#create lecturer_api api here
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturer_api(request):
    if request.method == 'GET':
        lecturers = Lecturer.objects.all()
        lecturer_serializer = LecturerSerializer(lecturers, many=True)
        return Response(lecturer_serializer.data)
    

#create lecturer_detail api here
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturer_detail(request, pk):
    try:
        lecturer = Lecturer.objects.get(pk=pk)
    except Lecturer.DoesNotExist:
        return Response({'error': 'Lecturer does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        lecturer_serializer = LecturerSerializer(lecturer)
        return Response(lecturer_serializer.data)

    elif request.method == 'PUT':
        user_data = {}
        
        if 'username' in request.data and request.data['username'] != lecturer.admin.username:
            user_data['username'] = request.data['username']
        if 'first_name' in request.data and request.data['first_name'] != lecturer.admin.first_name:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data and request.data['last_name'] != lecturer.admin.last_name:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data and request.data['email'] != lecturer.admin.email:
            user_data['email'] = request.data['email']
        if 'password' in request.data and request.data['password'] != lecturer.admin.password:
            user_data['password'] = request.data['password']
        if 'user_type' in request.data and request.data['user_type'] != lecturer.admin.user_type:
            user_data['user_type'] = request.data['user_type']

        lecturer_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            lecturer_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("phone_number"):
            lecturer_data["phone_number"] = request.data.get("phone_number")
        if request.data.get("role"):
            lecturer_data["role"] = request.data.get("role")

        lecturer_serializer = LecturerSerializer(lecturer, data=lecturer_data, partial=True)
        if lecturer_serializer.is_valid():
            lecturer_serializer.save()
            return Response(lecturer_serializer.data)
        return Response(lecturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user = CustomUser.objects.get(username=lecturer.admin.username)
        user.delete()
        lecturer.delete()
        return Response({'success': 'Lecturer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)