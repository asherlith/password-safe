from django.shortcuts import render
from .models import Password, User
from .serializers import UserSerializer, PasswordSerializer, RegisterSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class KeyGeneratorAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        key = Fernet.generate_key()
        return Response({"key": key})


class PasswordAPI(GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        key = Fernet.generate_key()
        f = Fernet(key)
        password = f.encrypt(request.data.get("password").encode())
        data = {"user": request.data.get("user"),
                "password": str(password),
                "title": request.data.get("title"),
                "website": request.data.get("website"),
                "key": str(key)
                }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        password = serializer.save()
        return Response({
            "password": PasswordSerializer(password, context= {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'key' :key
        }
).data,
        })


class AllUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
