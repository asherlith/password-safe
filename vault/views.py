from django.shortcuts import render
from .models import Password
from .serializers import UserSerializer, PasswordSerializer, RegisterSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


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
    pass
