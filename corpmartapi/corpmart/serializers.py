import datetime as dt
import json
from rest_framework import exceptions
from rest_framework import serializers
from .models import OneTimePassword, User, Business, ContactRequest, Balancesheet, ViewHistory, ChatbotRequest, Blog, \
    Testimonial
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


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


class PostBusinessSerializer(serializers.ModelSerializer):
    posted_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Business
        exclude = ['is_verified', 'admin_defined_selling_price', 'verified_by']


# Used for listing the businesses
class BusinessListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'sale_description', 'company_type', 'sub_type', 'sub_type_others_description', 'industry',
                  'industries_others_description', 'state', 'authorised_capital', 'paidup_capital',
                  'admin_defined_selling_price']


class BusinessDetailSerializer(serializers.ModelSerializer):
    balancesheet_available = serializers.SerializerMethodField(read_only=True)
    balancesheet_id = serializers.SerializerMethodField(read_only=True)
    has_contacted = serializers.SerializerMethodField(read_only=True)
    # has_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Business
        fields = ['id', 'sale_description', 'company_type', 'sub_type', 'sub_type_others_description', 'industry',
                  'industries_others_description', 'year_of_incorporation', 'state',
                  'authorised_capital', 'paidup_capital', 'admin_defined_selling_price', 'has_gst_number',
                  'has_bank_account', 'has_import_export_code', 'has_other_license', 'other_license', 'has_contacted',
                  'balancesheet_available', 'balancesheet_id']

    @staticmethod
    def get_balancesheet_available(obj):
        b = Balancesheet.objects.filter(business__id=obj.id).first()
        if b is not None:
            return True
        else:
            return False

    def get_has_contacted(self, obj):
        # contacted = None
        try:
            if self.context['request'].user.is_authenticated:
                user = self.context['request'].user
                contacted = ContactRequest.objects.filter(requested_by=user, business__id=obj.id).first()
            else:
                contacted = None
        except ObjectDoesNotExist:
            return False

        if contacted is not None:
            return True
        else:
            return False

    # def get_has_paid(self, obj):
    #     user = self.context['request'].user
    #     b = Balancesheet.objects.filter(pk=obj.id).first()
    #     if b is not None:
    #         bp = BalancesheetPayment.objects.filter(balancesheet=b, user=user, payment_successful=True).first()
    #         if bp is not None:
    #             return bp.payment_successful
    #         else:
    #             return False
    #     else:
    #         return False

    def get_balancesheet_id(self, obj):
        b = Balancesheet.objects.filter(business__id=obj.id).first()
        if b is not None:
            return b.id
        else:
            return None


class ContactRequestSerializer(serializers.ModelSerializer):
    requested_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    business = BusinessListSerializer

    class Meta:
        model = ContactRequest
        fields = ['requested_by', 'business']


class BalancesheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Balancesheet
        fields = ['file']


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonial
        fields = '__all__'


class ViewHistorySerializer(serializers.ModelSerializer):
    viewed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    business = BusinessDetailSerializer

    class Meta:
        model = ViewHistory
        fields = '__all__'
        depth = 1


class ChatbotRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotRequest
        fields = ['name', 'email', 'mobile', 'query']
