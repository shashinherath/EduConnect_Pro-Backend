from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Admin, Lecturer, Course, Student, Chat, LectureMaterial
from .serializers import AdminSerializer, CourseSerializer, LectureMaterialSerializer, LecturerSerializer, StudentSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, parser_classes
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
    return Response({'success': 'User logged out successfully'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    if user.user_type == "1":
        admin = Admin.objects.get(admin=user)
        admin_serializer = AdminSerializer(admin)
        return Response(admin_serializer.data)
    elif user.user_type == "2":
        lecturer = Lecturer.objects.get(admin=user)
        lecturer_serializer = LecturerSerializer(lecturer)
        return Response(lecturer_serializer.data)
    elif user.user_type == "3":
        student = Student.objects.get(admin=user)
        student_serializer = StudentSerializer(student)
        return Response(student_serializer.data)
    return Response({'error': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)



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
            user_data['password'] = make_password(request.data['password'])
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
        if 'password' in request.data and make_password(request.data['password']) != admin.admin.password:
            user_data['password'] = make_password(request.data['password'])
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
            user_data['password'] = make_password(request.data['password'])
        if 'user_type' in request.data:
            user_data['user_type'] = request.data['user_type']

        lecturer_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            lecturer_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("degree"):
            lecturer_data["degree"] = request.data.get("degree")
        if request.data.get("role"):
            lecturer_data["role"] = request.data.get("role")

        lecturer_serializer = LecturerSerializer(data=lecturer_data, partial=True)
        if lecturer_serializer.is_valid():
            lecturer_serializer.save()
            return Response(lecturer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(lecturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturer_api(request):
    if request.method == 'GET':
        lecturers = Lecturer.objects.all()
        lecturer_serializer = LecturerSerializer(lecturers, many=True)
        return Response(lecturer_serializer.data)
    


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
        if 'password' in request.data and make_password(request.data['password']) != lecturer.admin.password:
            user_data['password'] = make_password(request.data['password'])
        if 'user_type' in request.data and request.data['user_type'] != lecturer.admin.user_type:
            user_data['user_type'] = request.data['user_type']

        lecturer_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            lecturer_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("degree"):
            lecturer_data["degree"] = request.data.get("degree")
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
    

#student_add api
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def student_add(request):
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
            user_data['password'] = make_password(request.data['password'])
        if 'user_type' in request.data:
            user_data['user_type'] = request.data['user_type']

        student_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            student_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("phone_number"):
            student_data["phone_number"] = request.data.get("phone_number")
        if request.data.get("degree"):
            student_data["degree"] = request.data.get("degree")

        student_serializer = StudentSerializer(data=student_data, partial=True)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#student_api
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_api(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_serializer = StudentSerializer(students, many=True)
        return Response(student_serializer.data)
    

#student_detail api
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        student_serializer = StudentSerializer(student)
        return Response(student_serializer.data)

    elif request.method == 'PUT':
        user_data = {}
        
        if 'username' in request.data and request.data['username'] != student.admin.username:
            user_data['username'] = request.data['username']
        if 'first_name' in request.data and request.data['first_name'] != student.admin.first_name:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data and request.data['last_name'] != student.admin.last_name:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data and request.data['email'] != student.admin.email:
            user_data['email'] = request.data['email']
        if 'password' in request.data and make_password(request.data['password']) != student.admin.password:
            user_data['password'] = make_password(request.data['password'])
        if 'user_type' in request.data and request.data['user_type'] != student.admin.user_type:
            user_data['user_type'] = request.data['user_type']

        student_data = { "admin": user_data}

        if request.data.get("profile_pic"):
            student_data["profile_pic"] = request.data.get("profile_pic")
        if request.data.get("phone_number"):
            student_data["phone_number"] = request.data.get("phone_number")
        if request.data.get("degree"):
            student_data["degree"] = request.data.get("degree")

        student_serializer = StudentSerializer(student, data=student_data, partial=True)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user = CustomUser.objects.get(username=student.admin.username)
        user.delete()
        student.delete()
        return Response({'success': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    


#course_add api
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def course_add(request):
    if request.method == 'POST':
        course_data = {}
        if 'name' in request.data:
            course_data['name'] = request.data['name']
        if 'description' in request.data:
            course_data['description'] = request.data['description']
        if 'image' in request.data:
            course_data['image'] = request.data['image']
        if 'degree' in request.data:
            course_data['degree'] = request.data['degree']

        course_serializer = CourseSerializer(data=course_data, partial=True)
        if course_serializer.is_valid():
            course_serializer.save()
            return Response(course_serializer.data, status=status.HTTP_201_CREATED)
        return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#course_api
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def course_api(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        course_serializer = CourseSerializer(courses, many=True)
        return Response(course_serializer.data)
    

#course_detail api
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        course_serializer = CourseSerializer(course)
        return Response(course_serializer.data)

    elif request.method == 'PUT':
        course_data = {}
        
        if 'name' in request.data and request.data['name'] != course.name:
            course_data['name'] = request.data['name']
        if 'description' in request.data and request.data['description'] != course.description:
            course_data['description'] = request.data['description']
        if 'image' in request.data and request.data['image'] != course.image:
            course_data['image'] = request.data['image']
        if 'degree' in request.data and request.data['degree'] != course.degree:
            course_data['degree'] = request.data['degree']

        course_serializer = CourseSerializer(course, data=course_data, partial=True)
        if course_serializer.is_valid():
            course_serializer.save()
            return Response(course_serializer.data)
        return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response({'success': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

#lecture material add api
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def lecture_material_add(request):
    if request.method == 'POST':
        lecture_material_data = {}
        if 'title' in request.data:
            lecture_material_data['title'] = request.data['title']
        if 'description' in request.data:
            lecture_material_data['description'] = request.data['description']
        if 'file' in request.data:
            lecture_material_data['file'] = request.data['file']
        if 'course_id' in request.data:
            lecture_material_data['course_id'] = request.data['course_id']

        lecture_material_serializer = LectureMaterialSerializer(data=lecture_material_data, partial=True)
        if lecture_material_serializer.is_valid():
            lecture_material_serializer.save()
            return Response(lecture_material_serializer.data, status=status.HTTP_201_CREATED)
        return Response(lecture_material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#lecture_material_api
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecture_material_api(request):
    if request.method == 'GET':
        lecture_materials = LectureMaterial.objects.all()
        lecture_material_serializer = LectureMaterialSerializer(lecture_materials, many=True)
        return Response(lecture_material_serializer.data)
    

#lecture_material_detail api
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecture_material_detail(request, pk):
    try:
        lecture_material = LectureMaterial.objects.get(pk=pk)
    except LectureMaterial.DoesNotExist:
        return Response({'error': 'Lecture Material does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        lecture_material_serializer = LectureMaterialSerializer(lecture_material)
        return Response(lecture_material_serializer.data)

    elif request.method == 'PUT':
        lecture_material_data = {}
        
        if 'title' in request.data and request.data['title'] != lecture_material.title:
            lecture_material_data['title'] = request.data['title']
        if 'description' in request.data and request.data['description'] != lecture_material.description:
            lecture_material_data['description'] = request.data['description']
        if 'file' in request.data and request.data['file'] != lecture_material.file:
            lecture_material_data['file'] = request.data['file']
        if 'course_id' in request.data and request.data['course_id'] != lecture_material.course_id:
            lecture_material_data['course_id'] = request.data['course_id']

        lecture_material_serializer = LectureMaterialSerializer(lecture_material, data=lecture_material_data, partial=True)
        if lecture_material_serializer.is_valid():
            lecture_material_serializer.save()
            return Response(lecture_material_serializer.data)
        return Response(lecture_material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lecture_material.delete()
        return Response({'success': 'Lecture Material deleted successfully'}, status=status.HTTP_204_NO_CONTENT)