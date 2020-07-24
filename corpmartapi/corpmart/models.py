from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


# https://tech.serhatteker.com/post/2020-01/email-as-username-django/
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, mobile, password="", **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        if not mobile:
            raise ValueError(_('The Mobile number must be set'))
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, mobile, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.model(
            email=self.normalize_email(email)
        )
        user.mobile= mobile
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    country_code = models.IntegerField(default=91)
    mobile = models.IntegerField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email},{self.mobile}"


class OneTimePassword(models.Model):
    otp = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="onetimepassword", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


class Business(models.Model):
    STATE_LIST = (
        ('Assam', 'Assam'),
        ('Delhi', 'Delhi'),
    )
    COMPANY_TYPE_LIST = (
        ('LTD', 'LTD'),
        ('LLC', 'LLC'),
    )
    SUB_TYPE_LIST = (
        ('LTD', 'LTD'),
        ('LLC', 'LLC'),
    )
    INDUSTRY_LIST = (
        ('TEXTILE', 'TEXTILE'),
        ('STEEL', 'STEEL'),
    )

    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='businesses', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=500)
    state = models.CharField(max_length=100, choices=STATE_LIST, default='Assam')
    country = models.CharField(max_length=100, default='India')
    company_type = models.CharField(max_length=200, choices=COMPANY_TYPE_LIST, default='LTD')
    sub_type = models.CharField(max_length=200, choices=SUB_TYPE_LIST, default='LTD')
    industry = models.CharField(max_length=200, choices=INDUSTRY_LIST, default='TEXTILE')
    sale_description = models.CharField(max_length=500, blank=True)
    year_of_incorporation = models.IntegerField(null=True, blank=True)
    has_gst_number = models.BooleanField(null=True)
    has_import_export_code = models.BooleanField(null=True)
    has_bank_account = models.BooleanField(null=True)
    has_other_license = models.BooleanField(null=True)
    other_license = models.CharField(max_length=500, blank=True)
    capital = models.IntegerField(null=True, blank=True)
    user_defined_selling_price = models.IntegerField(null=True, blank=True)
    admin_defined_selling_price = models.IntegerField(null=True, blank=True)


class Balancesheet(models.Model):
    business = models.ForeignKey(Business, related_name='balancesheets', on_delete=models.CASCADE)
    file = models.FileField(upload_to='balancesheet')
    uploaded_on = models.DateTimeField(auto_now_add=True)


class BalancesheetPayment(models.Model):
    balancesheet = models.ForeignKey(Balancesheet, related_name='balancesheetpayments', on_delete=models.CASCADE)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='balancesheetpayments', on_delete=models.CASCADE)
    paid_on = models.DateTimeField(auto_now_add=True)
    paid_amount = models.IntegerField()
    transaction_id = models.IntegerField()


class Blog(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_text = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='profile_picture', blank=True)
