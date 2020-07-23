from random import randint
import requests
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework import viewsets, views, generics
from rest_framework.authtoken.models import Token
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
        mobile = request.data.get("mobile")
        otp = request.data.get('otp')

        if email:
            user = User.objects.get(email=email)
        elif mobile:
            user = User.objects.get(mobile=mobile)

        otp_object = OneTimePassword.objects.get(user=user)
        if otp_object.otp == otp:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "id": user.id, "mobile": user.mobile, "email": user.email},)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class GenerateOTPView(APIView):
    permission_classes = ()

    def post(self, request, ):
        email = request.data.get("email")
        mobile = request.data.get("mobile")
        if email:
            user = User.objects.get(email=email)
        elif mobile:
            user = User.objects.get(mobile=mobile)

        random_otp = randint(10000, 99999)

        if user:
            obj, created = OneTimePassword.objects.update_or_create(
                user=user,
                defaults={'otp': random_otp},
            )
            # For Email-------------------------------------------------------------------------------------------------
            # https://www.twilio.com/blog/using-twilio-sendgrid-send-emails-python-django
            otp_string = f"Your OTP for CorpMart is {random_otp}."
            send_mail("OTP for CorpMart", otp_string, "paramchauhan21@gmail.com", [user.email])
            # End Email-------------------------------------------------------------------------------------------------

            # For SMS---------------------------------------------------------------------------------------------------
            # https://docs.fast2sms.com/#post
            url = "https://www.fast2sms.com/dev/bulk"
            var = "{#AA#}"
            payload = f"sender_id=FSTSMS&language=english&route=qt&numbers={user.mobile}&message=32122&variables={var}&variables_values={random_otp}"
            headers = {
                'authorization': "liDGeo7BY84UcEmWIQxZCA0qFJjMS5nfkug6NwL1OvpHVaTyr35QimMDA3EVvXpS4FyskUIeH6TGw12r",
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
            }

            resp = requests.request("POST", url, data=payload, headers=headers)
            # print(resp.text)
            # End SMS---------------------------------------------------------------------------------------------------
            return Response({"token_for_testing": random_otp}, )
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
