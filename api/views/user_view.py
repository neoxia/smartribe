from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.serializers.serializers import UserSerializer
from api.serializers.serializers import UserCreateSerializer
from api.authenticate import AuthUser


class UserViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny]
    model = User

    def create(self, request):
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        serial_user = UserCreateSerializer(data=data)
        if serial_user.is_valid():
            serial_user.save()
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user, response = AuthUser().authenticate(request)
        forbidden = status.HTTP_403_FORBIDDEN
        if not user:
            return response
        elif str(user.id) != pk:
            return Response({"detail": "Access denied"}, status=forbidden)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user, response = AuthUser().authenticate(request)
        forbidden = status.HTTP_403_FORBIDDEN
        if not user:
            return response
        elif str(user.id) != pk:
            return Response({"detail": "Access denied"}, status=forbidden)
        data = JSONParser().parse(request)
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serial_user = UserSerializer(user, data=data, partial=True)
        if serial_user.is_valid():
            serial_user.save()
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user, response = AuthUser().authenticate(request)
        if not user:
            return response
        serializer = UserSerializer(user)
        return Response(serializer.data)



