from random import randint
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, OneTimePassword
from .serializers import UserSerializer
# Create your views here.


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        email = request.data.get("email")
        otp = request.data.get('otp')
        # password = request.data.get("password")
        user = User.objects.get(email=email)
        existing_otp = OneTimePassword.objects.get(user__email=email)
        if existing_otp == otp:
            return Response({"token": user.auth_token.key, "id": user.id},)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class GenerateOTPMobileView(APIView):
    permission_classes = ()

    def post(self, request,):
        mobile = request.data.get("mobile")
        user = User.objects.get(mobile=mobile)
        random_otp = randint(10000, 99999)
        if user:
            user.onetimepassword_set.otp = random_otp
            return Response({"token": random_otp},)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Allow users to be viewed/edited
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        # email = self.request.query_params.get('email')
        user_id = self.request.query_params.get('user_id')
        # token = self.request.authenticators
        queryset = User.objects.filter(id=1)
        # if not validate_email(email):
        #     queryset = User.objects.filter(email=email)
        if user_id:
            queryset = User.objects.filter(id=user_id)
        return queryset
