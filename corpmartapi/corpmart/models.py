from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from markdownx.models import MarkdownxField


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


# TODO: exclude fieds like staff_status from admin dashboard
class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    country_code = models.IntegerField(default=91)
    mobile = models.BigIntegerField(unique=True)
    organisation_name = models.CharField(max_length=200, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email} | {self.mobile}"


class OneTimePassword(models.Model):
    otp = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="onetimepassword", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


class Business(models.Model):
    STATE_LIST = (("Andhra Pradesh","Andhra Pradesh"),
                  ("Arunachal Pradesh","Arunachal Pradesh"),
                  ("Assam","Assam"),("Bihar","Bihar"),
                  ("Chhattisgarh","Chhattisgarh"),
                  ("Goa","Goa"),
                  ("Gujarat","Gujarat"),
                  ("Haryana","Haryana"),
                  ("Himachal Pradesh","Himachal Pradesh"),
                  ("Jammu and Kashmir","Jammu and Kashmir"),
                  ("Jharkhand","Jharkhand"),
                  ("Karnataka","Karnataka"),
                  ("Kerala","Kerala"),
                  ("Madhya Pradesh","Madhya Pradesh"),
                  ("Maharashtra","Maharashtra"),
                  ("Manipur","Manipur"),
                  ("Meghalaya","Meghalaya"),
                  ("Mizoram","Mizoram"),
                  ("Nagaland","Nagaland"),
                  ("Odisha","Odisha"),
                  ("Punjab","Punjab"),
                  ("Rajasthan","Rajasthan"),
                  ("Sikkim","Sikkim"),
                  ("Tamil Nadu","Tamil Nadu"),
                  ("Telangana","Telangana"),
                  ("Tripura","Tripura"),
                  ("Uttar Pradesh","Uttar Pradesh"),
                  ("Uttarakhand","Uttarakhand"),
                  ("West Bengal","West Bengal"),
                  ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
                  ("Chandigarh","Chandigarh"),
                  ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
                  ("Daman and Diu","Daman and Diu"),
                  ("Lakshadweep","Lakshadweep"),
                  ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
                  ("Puducherry","Puducherry"),
                  ('Ladakh','Ladakh'),)

    COMPANY_TYPE_LIST = (
        ('Pvt. Ltd.', 'Pvt. Ltd.'),
        ('Limited Liability Partnership (LLP)', 'Limited Liability Partnership (LLP)'),
        ('Partnership Firm', 'Partnership Firm'),
        ('Trust/Society', 'Trust/Society'),
        ('Others', 'Others'),
    )
    SUB_TYPE_LIST = (
        ('One Person Company', 'One Person Company'),
        ('Producer Company', 'Producer Company'),
        ('Nidhi Company', 'Nidhi Company'),
        ('Section-8 Company(NGO)', 'Section-8 Company(NGO)'),
        ('Non-Banking Financial Company (NBFC)','Non-Banking Financial Company (NBFC)'),
        ('Micro-Finance Company', 'Micro-Finance Company'),
        ('Insurance Company', 'Insurance Company'),
        ('Direct Selling Company', 'Direct Selling Company'),
        ('Others', 'Others'),
    )
    INDUSTRY_LIST = (
        ('AGRICULTURE AND ALLIED INDUSTRIES','AGRICULTURE AND ALLIED INDUSTRIES'),
        ('AUTOMOBILES', 'AUTOMOBILES'),
        ('AUTO COMPONENTS', 'AUTO COMPONENTS'),
        ('AVIATION', 'AVIATION'),
        ('BANKING', 'BANKING'),
        ('CEMENT', 'CEMENT'),
        ('CONSUMER DURABLES', 'CONSUMER DURABLES'),
        ('CONSULTING', 'CONSULTING'),
        ('ECOMMERCE', 'ECOMMERCE'),
        ('EDUCATION AND TRAINING', 'EDUCATION AND TRAINING'),
        ('ENGINEERING AND CAPITAL GOODS', 'ENGINEERING AND CAPITAL GOODS'),
        ('FINANCIAL SERVICES', 'FINANCIAL SERVICES'),
        ('FMCG', 'FMCG'),
        ('GEMS AND JEWELLERY', 'GEMS AND JEWELLERY'),
        ('HEALTHCARE', 'HEALTHCARE'),
        ('INFRASTRUCTURE', 'INFRASTRUCTURE'),
        ('INSURANCE', 'INSURANCE'),
        ('IT & ITES', 'IT & ITES'),
        ('MANUFACTURING', 'MANUFACTURING'),
        ('MEDIA AND ENTERTAINMENT', 'MEDIA AND ENTERTAINMENT'),
        ('METALS AND MINING', 'METALS AND MINING'),
        ('OIL AND GAS', 'OIL AND GAS'),
        ('PHARMACEUTICALS', 'PHARMACEUTICALS'),
        ('PORTS', 'PORTS'),
        ('POWER', 'POWER'),
        ('RAILWAYS', 'RAILWAYS'),
        ('REAL ESTATE', 'REAL ESTATE'),
        ('RENEWABLE ENERGY', 'RENEWABLE ENERGY'),
        ('RETAIL', 'RETAIL'),
        ('ROADS', 'ROADS'),
        ('SCIENCE AND TECHNOLOGY', 'SCIENCE AND TECHNOLOGY'),
        ('SERVICES', 'SERVICES'),
        ('STEEL', 'STEEL'),
        ('TELECOMMUNICATIONS', 'TELECOMMUNICATIONS'),
        ('TEXTILES', 'TEXTILES'),
        ('TRADING', 'TRADING'),
        ('TOURISM AND HOSPITALITY', 'TOURISM AND HOSPITALITY'),
        ('OTHERS', 'OTHERS')

    )

    is_verified = models.BooleanField()
    verified_by = models.CharField(max_length=30, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='businesses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    business_name = models.CharField(max_length=500)
    state = models.CharField(max_length=100, choices=STATE_LIST, null=True, blank=True)
    country = models.CharField(max_length=100, default='India')
    company_type = models.CharField(max_length=200, choices=COMPANY_TYPE_LIST, null=True, blank=True)
    company_type_others_description = models.CharField(max_length=500, blank=True, null=True)
    sub_type = models.CharField(max_length=200, choices=SUB_TYPE_LIST, null=True, blank=True)
    sub_type_others_description = models.CharField(max_length=500, blank=True, null=True)
    industry = models.CharField(max_length=200, choices=INDUSTRY_LIST, null=True, blank=True)
    industries_others_description = models.CharField(max_length=500, blank=True, null=True)
    sale_description = models.CharField(max_length=500, blank=True)
    year_of_incorporation = models.IntegerField(null=True, blank=True)
    has_gst_number = models.BooleanField(null=True)
    has_import_export_code = models.BooleanField(null=True)
    has_bank_account = models.BooleanField(null=True)
    has_other_license = models.BooleanField(null=True)
    other_license = models.CharField(max_length=500, blank=True)
    authorised_capital = models.IntegerField(null=True, blank=True)
    paidup_capital = models.IntegerField(null=True, blank=True)
    user_defined_selling_price = models.IntegerField(null=True, blank=True)
    admin_defined_selling_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} | NAME: {self.business_name}"

    class Meta:
        verbose_name_plural = 'Businesses'


class Balancesheet(models.Model):
    business = models.OneToOneField(Business, related_name='balancesheets', on_delete=models.CASCADE)
    file = models.FileField(upload_to='balancesheet')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Business: {self.business}"


# Model to keep track of balancesheet orders
# class BalancesheetPayment(models.Model):
#     # transaction_id will be created each time "buy" button is pressed
#     transaction_id = models.AutoField(primary_key=True)
#     balancesheet = models.ForeignKey(Balancesheet, related_name='balancesheetpayments', on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='balancesheetpayments', on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     amount = models.IntegerField()
#     # when order is created, the returned order_id is stored here
#     order_id = models.CharField(max_length=200, unique=True)
#     # the following field is available only on successfull payment
#     payment_successful = models.BooleanField(null=True)
#     razorpay_payment_id = models.CharField(max_length=200, blank=True)
#     razorpay_order_id = models.CharField(max_length=200, blank=True)
#     razorpay_signature = models.CharField(max_length=500, blank=True)


class Blog(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_text = MarkdownxField()
    picture = models.ImageField(upload_to='blog_picture', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.CharField(max_length=100)

    def __str__(self):
        return self.blog_title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='profile_picture', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactRequest(models.Model):
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contactrequests', on_delete=models.CASCADE)
    business = models.ForeignKey(Business, related_name='contact_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)
    processed_by = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("requested_by", "business")

    def __str__(self):
        return f"Requested by -> {self.requested_by} || Business -> {self.business}"


class ViewHistory(models.Model):
    business = models.ForeignKey(Business, related_name='viewhistory', on_delete=models.CASCADE)
    viewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='viewhistory', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ViewHistory'

    def __str__(self):
        return f"Viewed by -> {self.viewed_by} || Business -> {self.business}"


class ChatbotRequest(models.Model):
    name = models.CharField(max_length=100, blank=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True)
    query = models.CharField(max_length=5000)
    # Following for admin
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_by = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Requested by -> {self.name} || Mobile -> {self.mobile} || Email -> {self.email}"


class ChatbotNotification(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Name -> {self.name} || Mobile -> {self.mobile} || Email -> {self.email}"
