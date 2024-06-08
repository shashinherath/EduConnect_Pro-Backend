from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_superuser:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Only superusers can log in'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)