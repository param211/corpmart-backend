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
from .models import User, OneTimePassword, Business, Balancesheet, BalancesheetPayment
from .serializers import UserSerializer, SignupSerializer, BusinessListSerializer, BusinessDetailSerializer, \
    PostBusinessSerializer, ContactRequestSerializer, BalancesheetSerializer
# Razorpay settings
import razorpay
client = razorpay.Client(auth=("rzp_test_IjDKOxNLcSy87u", "HbmWwNZELof6dfhRWm7jwKMZ"))
# Create your views here.


class SignupView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignupSerializer


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
            # # For Email-------------------------------------------------------------------------------------------------
            # # https://www.twilio.com/blog/using-twilio-sendgrid-send-emails-python-django
            # otp_string = f"Your OTP for CorpMart is {random_otp}."
            # send_mail("OTP for CorpMart", otp_string, "paramchauhan21@gmail.com", [user.email])
            # # End Email-------------------------------------------------------------------------------------------------
            #
            # # For SMS---------------------------------------------------------------------------------------------------
            # # https://docs.fast2sms.com/#post
            # url = "https://www.fast2sms.com/dev/bulk"
            # var = "{#AA#}"
            # payload = f"sender_id=FSTSMS&language=english&route=qt&numbers={user.mobile}&message=32122&variables={var}&variables_values={random_otp}"
            # headers = {
            #     'authorization': "liDGeo7BY84UcEmWIQxZCA0qFJjMS5nfkug6NwL1OvpHVaTyr35QimMDA3EVvXpS4FyskUIeH6TGw12r",
            #     'cache-control': "no-cache",
            #     'content-type': "application/x-www-form-urlencoded"
            # }
            #
            # resp = requests.request("POST", url, data=payload, headers=headers)
            # # print(resp.text)
            # # End SMS---------------------------------------------------------------------------------------------------
            return Response({"otp_for_testing": random_otp}, )
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allow users to be viewed, get by ?user_id, user_ mobile and user_email
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        user_email = self.request.query_params.get('user_email')
        user_mobile = self.request.query_params.get("user_mobile")
        queryset = User.objects.none()
        if user_id:
            queryset = User.objects.filter(id=user_id)
        elif user_email:
            queryset = User.objects.filter(email=user_email)
        elif user_mobile:
            queryset = User.objects.filter(mobile=user_mobile)
        return queryset


class PostBusiness(generics.CreateAPIView):
    """
    Allows to post business
    """
    serializer_class = PostBusinessSerializer


class BusinessListViewset(viewsets.ReadOnlyModelViewSet):
    """
    Allows business list to be viewed and queried
    """
    serializer_class = BusinessListSerializer
    queryset = Business.objects.all()


class BusinessDetailViewset(viewsets.ReadOnlyModelViewSet):
    """
    Allows business detail to be viewed
    """
    serializer_class = BusinessDetailSerializer
    queryset = Business.objects.all()


class ContactRequest(generics.CreateAPIView):
    """
    Allows to post contact requests
    """
    serializer_class = ContactRequestSerializer


# For creating a order through razorpay. Order is created when user clicks on the payment button
# The order details are posted to razorpay and order_id is returned
class OrderBalancesheet(APIView):

    def post(self, request,):
        business_id = request.data.get("business_id")
        user = request.user

        # For razorpay note
        ordered_by = f"Name: {user.first_name} {user.last_name}, Mobile: {user.mobile}"

        # razorpay variables
        order_amount = 50000
        order_currency = 'INR'
        notes = {'ordered_by': ordered_by}

        response = client.order.create(amount=order_amount, currency=order_currency, notes=notes, payment_capture='1')
        order_id = response['id']

        if order_id:
            balancesheet = Balancesheet.objects.get(business__id=business_id)
            b = BalancesheetPayment(balancesheet=balancesheet, user=user, order_id=order_id)
            b.save()
            return Response({"order_id": order_id}, )

        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class SuccessfulPayment(APIView):

    def post(self, request, ):
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_signature = request.data.get("razorpay_signature")
        order_id = request.data.get("order_id")

        b = BalancesheetPayment.objects.get(order_id=order_id)
        b.razorpay_payment_id = razorpay_payment_id
        b.razorpay_order_id = razorpay_order_id
        b.razorpay_signature = razorpay_signature

        params_dictionary = {'razorpay_order_id': order_id, 'razorpay_payment_id': razorpay_payment_id,
                             'razorpay_signature': razorpay_signature}
        verify = client.utility.verify_payment_signature(params_dictionary)

        if verify:
            b.payment_sucessful = True
            b.save()
            return Response({"success": "Payment signature verified.", "balancesheet_id": b.balancesheet__id},)

        else:
            b.payment_sucessful = False
            b.save()
            return Response({"error": "Payment signature is wrong, possible malicious attempt."},
                            status=status.HTTP_400_BAD_REQUEST)


class BalancesheetViewset(viewsets.ReadOnlyModelViewSet):
    """
    For viewing balancesheets
    """
    serializer_class = BalancesheetSerializer

    def get_queryset(self):
        queryset = Balancesheet.objects.none()
        user = self.request.user
        balancesheet_id = self.request.query_params.get('balancesheet_id')
        b = Balancesheet.objects.get(pk=balancesheet_id)
        bp = BalancesheetPayment.objects.get(balancesheet=b, user=user)
        has_paid = bp.payment_sucessful

        if has_paid:
            queryset = Balancesheet.objects.filter(id=balancesheet_id)

        return queryset
