import datetime as dt
import json
from rest_framework import exceptions
from rest_framework import serializers
from .models import OneTimePassword, User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        # https://github.com/encode/django-rest-framework/issues/1249
        model = User
        fields = ['email', 'first_name', 'last_name', 'country_code', 'mobile', 'organisation_name']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'], first_name=validated_data['first_name'],
            last_name=validated_data['last_name'], country_code=validated_data['country_code'],
            mobile=validated_data['mobile'], organisation_name=validated_data['organisation_name']
        )
        user.save()
        Token.objects.create(user=user)
        return user


class OneTimePasswordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = OneTimePassword
        fields = '__all__'
        depth = 1
