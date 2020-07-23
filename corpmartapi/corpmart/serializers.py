import datetime as dt
import json
from rest_framework import exceptions
from rest_framework import serializers
from .models import OneTimePassword, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OneTimePasswordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = OneTimePassword
        fields = '__all__'
        depth = 1
