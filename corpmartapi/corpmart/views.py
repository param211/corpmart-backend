from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import permissions
from .serializers import MobileTokenObtainPairSerializer, EmailTokenObtainPairSerializer
# Create your views here.


# Custom simple_jwt view for bypassing password validation
class MyTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        if ("otp" in self.request.data) and ("mobile" in self.request.data):
            return MobileTokenObtainPairSerializer
        elif ("otp" in self.request.data) and ("email" in self.request.data):
            return EmailTokenObtainPairSerializer
        return TokenObtainPairSerializer
