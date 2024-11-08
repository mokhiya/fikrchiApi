import random

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser


class VerifyEmail(APIView):
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email, verification_code=code)
            user.email_verified = True
            user.verification_code = None
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCode(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            if user.email_verified:
                return Response({'message': 'Email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new code and send it
            user.verification_code = str(random.randint(1000, 9999))
            user.save()
            user.send_verification_email()
            return Response({'message': 'Verification code resent.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
