from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, VerifyEmail, ResendVerificationCode

app_name = 'users'

urlpatterns = [
    path('verify/', VerifyEmail.as_view(), name='verify_email'),
    path('verify/resend/', ResendVerificationCode.as_view(), name='resend_verification_code'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
]
