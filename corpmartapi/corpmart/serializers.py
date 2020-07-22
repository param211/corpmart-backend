from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime as dt
import json
from rest_framework import exceptions
from .models import OneTimePassword


# For obtaining token with mobile number and OTP
class MobileTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass
        else:
            request_data = json.loads(request.data)
            mobile = request_data.get("mobile")
            otp = request_data.get("otp")

            otp_does_not_exist = False
            try:
                otp_user = OneTimePassword.objects.get(user__mobile=mobile, otp=otp)
            except OneTimePassword.DoesNotExist:
                otp_does_not_exist = True
            else:
                time_elapsed = dt.datetime.now() - otp_user.created_at
                otp_does_not_exist = time_elapsed.total_seconds() > 900
            finally:
                if otp_does_not_exist:
                    error_message = "This OTP doesn't exist or has expired"
                    error_name = "wrong_otp"
                    raise exceptions.AuthenticationFailed(error_message, error_name)
        finally:
            return super().validate(attrs)


# For obtaining token with email and OTP
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass
        else:
            request_data = json.loads(request.data)
            email = request_data.get("email")
            otp = request_data.get("otp")

            otp_does_not_exist = False
            try:
                otp_user = OneTimePassword.objects.get(user__email=email, otp=otp)
            except OneTimePassword.DoesNotExist:
                otp_does_not_exist = True
            else:
                time_elapsed = dt.datetime.now() - otp_user.created_at
                otp_does_not_exist = time_elapsed.total_seconds() > 900
            finally:
                if otp_does_not_exist:
                    error_message = "This OTP doesn't exist or has expired"
                    error_name = "wrong_otp"
                    raise exceptions.AuthenticationFailed(error_message, error_name)
        finally:
            return super().validate(attrs)
