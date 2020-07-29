"""corpmartapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from corpmartapi.corpmart import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename="user")
router.register(r'business-list', views.BusinessListViewset, basename='business-list')
router.register(r'business-detail', views.BusinessDetailViewset, basename='business-detail')
router.register(r'balancesheet', views.BalancesheetViewset, basename='balancesheet')
router.register(r'view-history', views.ViewHistoryViewset, basename='view-history')

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/generate_otp/', views.GenerateOTPView.as_view(), name='generate_otp'),
    path('api/v1/login/', views.LoginView.as_view(), name="login"),
    path('api/v1/signup/', views.SignupView.as_view(), name="signup"),
    path('api/v1/post-business', views.PostBusiness.as_view(), name="post-business"),
    path('api/v1/contact-request', views.ContactRequest.as_view(), name="contact-request"),
    path('api/v1/max-price', views.MaxPriceView.as_view(), name="max-price"),
    # path('api/v1/orderbalancesheet', views.OrderBalancesheet.as_view(), name="orderbalancesheet"),
    # path('api/v1/successfulpayment', views.SuccessfulPayment.as_view(), name="successfulpayment")
]

# temporary, to view file from
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
