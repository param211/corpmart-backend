from random import randint
import datetime as dt
from django.db.models import Max
import requests
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework import filters
from rest_framework import viewsets, views, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, OneTimePassword, Business, Balancesheet, ViewHistory
from .serializers import UserSerializer, SignupSerializer, BusinessListSerializer, BusinessDetailSerializer, \
    PostBusinessSerializer, ContactRequestSerializer, BalancesheetSerializer, ViewHistorySerializer
# Razorpay settings
# import razorpay
# client = razorpay.Client(auth=("rzp_test_IjDKOxNLcSy87u", "HbmWwNZELof6dfhRWm7jwKMZ"))
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
            time_elapsed = dt.datetime.now(otp_object.updated_at.tzinfo) - otp_object.updated_at
            otp_not_expired = time_elapsed.total_seconds() < 900
            if otp_not_expired:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "id": user.id, "mobile": user.mobile, "email": user.email},)
            else:
                return Response({"error": "OTP expired. It is more than 15 minutes old."},
                                status=status.HTTP_400_BAD_REQUEST)

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

    def perform_create(self, serializer):
        serializer.save(admin_defined_selling_price=self.request.data.get('user_defined_selling_price'),
                        is_verified=False)


class BusinessListViewset(viewsets.ReadOnlyModelViewSet):
    """
    Allows business list to be viewed and queried
    """
    serializer_class = BusinessListSerializer
    permission_classes = ()

    # For search
    filter_backends = [filters.SearchFilter]
    search_fields = ['sale_description', 'state', 'company_type', 'company_type_others_description', 'sub_type',
                     'sub_type_others_description', 'industry', 'industries_others_description']

    def get_queryset(self):
        queryset = Business.objects.all()
        queryset = queryset.filter(is_verified=True)
        state = self.request.query_params.get('state')
        country = self.request.query_params.get('country')
        company_type = self.request.query_params.get('company_type')
        sub_type = self.request.query_params.get('sub_type')
        industry = self.request.query_params.get('industry')
        capital_max = self.request.query_params.get('capital_max')
        capital_min = self.request.query_params.get('capital_min')
        selling_price_max = self.request.query_params.get('selling_price_max')
        selling_price_min = self.request.query_params.get('selling_price_min')
        gst = self.request.query_params.get('gst')
        bank = self.request.query_params.get('bank')
        import_export_code = self.request.query_params.get('import_export_code')
        balancesheet = self.request.query_params.get('balancesheet')

        if state:
            queryset = queryset.filter(state=state)
        if company_type:
            queryset = queryset.filter(company_type=company_type)
        if country:
            queryset = queryset.filter(country=country)
        if sub_type:
            queryset = queryset.filter(sub_type=sub_type)
        if industry:
            queryset = queryset.filter(industry=industry)
        if capital_max:
            queryset = queryset.filter(capital__lte=capital_max)
        if capital_min:
            queryset = queryset.filter(capital__gte=capital_min)
        if selling_price_max:
            queryset = queryset.filter(admin_defined_selling_price__lte=selling_price_max)
        if selling_price_min:
            queryset = queryset.filter(admin_defined_selling_price__gte=selling_price_min)
        if gst:
            queryset = queryset.filter(has_gst_number=gst)
        if bank:
            queryset = queryset.filter(has_bank_account=bank)
        if import_export_code:
            queryset = queryset.filter(has_import_export_code=import_export_code)
        if balancesheet:
            queryset = queryset.filter(balancesheets__isnull=False)

        return queryset


class BusinessDetailViewset(viewsets.ReadOnlyModelViewSet):
    """
    Allows business detail to be viewed
    """
    serializer_class = BusinessDetailSerializer
    queryset = Business.objects.all()

    def get_queryset(self):
        user = self.request.user
        business_id = self.request.query_params.get('business_id')
        queryset = Business.objects.filter(id=business_id)

        # updating view history
        business = Business.objects.get(id=business_id)
        viewhistory, created = ViewHistory.objects.get_or_create(viewed_by=user, business=business)

        return queryset


class ContactRequest(generics.CreateAPIView):
    """
    Allows to post contact requests
    """
    serializer_class = ContactRequestSerializer


# For creating a order through razorpay. Order is created when user clicks on the payment button
# The order details are posted to razorpay and order_id is returned
# class OrderBalancesheet(APIView):
#
#     def post(self, request,):
#         business_id = request.data.get("business_id")
#         user = request.user
#
#         # For razorpay note
#         ordered_by = f"Name: {user.first_name} {user.last_name}, Mobile: {user.mobile}"
#
#         # razorpay variables
#         order_amount = 50000
#         order_currency = 'INR'
#         notes = {'ordered_by': ordered_by}
#
#         response = client.order.create(dict(amount=order_amount, currency=order_currency, notes=notes,
#                                             payment_capture='1'))
#         order_id = response['id']
#
#         if order_id:
#             balancesheet = Balancesheet.objects.get(business__id=business_id)
#             b = BalancesheetPayment(balancesheet=balancesheet, user=user, order_id=order_id, amount=order_amount)
#             b.save()
#             return Response({"order_id": order_id}, )
#
#         else:
#             return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SuccessfulPayment(APIView):
#
#     def post(self, request, ):
#         razorpay_payment_id = request.data.get("razorpay_payment_id")
#         razorpay_order_id = request.data.get("razorpay_order_id")
#         razorpay_signature = request.data.get("razorpay_signature")
#         order_id = request.data.get("order_id")
#
#         b = BalancesheetPayment.objects.get(order_id=order_id)
#         b.razorpay_payment_id = razorpay_payment_id
#         b.razorpay_order_id = razorpay_order_id
#         b.razorpay_signature = razorpay_signature
#
#         params_dictionary = {'razorpay_order_id': order_id, 'razorpay_payment_id': razorpay_payment_id,
#                              'razorpay_signature': razorpay_signature}
#         verify = client.utility.verify_payment_signature(params_dictionary)
#
#         if verify:
#             b.payment_sucessful = True
#             b.save()
#             return Response({"success": "Payment signature verified.", "balancesheet_id": b.balancesheet__id},)
#
#         else:
#             b.payment_sucessful = False
#             b.save()
#             return Response({"error": "Payment signature is wrong, possible malicious attempt."},
#                             status=status.HTTP_400_BAD_REQUEST)


class BalancesheetViewset(viewsets.ReadOnlyModelViewSet):
    """
    For viewing balancesheets
    """
    serializer_class = BalancesheetSerializer

    def get_queryset(self):
        # queryset = Balancesheet.objects.none()
        # user = self.request.user
        balancesheet_id = self.request.query_params.get('balancesheet_id')
        b = Balancesheet.objects.get(pk=balancesheet_id)
        # bp = BalancesheetPayment.objects.filter(balancesheet=b, user=user, payment_successful=True).first()
        # has_paid = bp.payment_sucessful

        # if has_paid:
        queryset = Balancesheet.objects.filter(id=balancesheet_id)

        return queryset


class ViewHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """
    For viewing balancesheets
    """
    serializer_class = ViewHistorySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ViewHistory.objects.filter(viewed_by=user).order_by('-viewed_at')

        return queryset


class MaxPriceView(APIView):
    permission_classes = ()

    def get(self, request,):
        """
        Return max price.
        """
        max_val = Business.objects.all().aggregate(
            Max('admin_defined_selling_price'))['admin_defined_selling_price__max']
        return Response(max_val)
