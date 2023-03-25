import base64
import os
from django.shortcuts import render
from .models import Password, User
from .serializers import UserSerializer, PasswordSerializer, RegisterSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from rest_framework import status


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class PasswordAPI(GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user_pwd = request.user.password.encode()
        print(user_pwd)
        salt = base64.b64encode(os.urandom(12))
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        hashed_pwd = base64.b64encode(kdf.derive(user_pwd))
        f = Fernet(hashed_pwd)
        password = f.encrypt(request.data.get("password").encode())
        data = {
            "user": request.user.pk,
            "password": password.decode(),
            "title": request.data.get("title"),
            "website": request.data.get("website"),
            "algo": 'pbkdf2_sha256',
            "iterations": '100000',
            "salt": salt.decode()
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        password = serializer.save()
        return Response({
            "password": PasswordSerializer(password, context={
                'request': self.request,
                'format': self.format_kwarg,
                'view': self
            }
                                           ).data
        }, status=status.HTTP_201_CREATED)


class UserPasswordAPI(GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        passwords = Password.objects.filter(user=request.user)
        return Response(PasswordSerializer(passwords, many=True).data)

    def post(self, request):
        user_pwd = request.user.password.encode()
        pass_id = request.data.get("pass_id")
        password = Password.objects.filter(pk=pass_id).first()
        if request.user == Password.objects.filter(pk=pass_id).first().user:
            kdf = PBKDF2HMAC(
                algorithm=SHA256(),
                length=32,
                salt=password.salt.encode(),
                iterations=int(password.iterations),
                backend=default_backend(),
            )
            key = base64.b64encode(kdf.derive(user_pwd))
            f = Fernet(key)

            secret = f.decrypt(password.password)
            return Response({"password": secret}, status=status.HTTP_200_OK)
        return Response({"error": "access denied"}, status=status.HTTP_401_UNAUTHORIZED)


class AllUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
