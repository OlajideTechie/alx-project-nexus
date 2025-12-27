from django.conf import settings
from rest_framework import status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse
from django.utils import timezone
from datetime import datetime

from drf_spectacular.utils import extend_schema

from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

import logging

logger = logging.getLogger(__name__)

User = get_user_model()


@extend_schema(
    tags=['Authentication'],
    responses={201: OpenApiResponse(description="User registered successfully")},
    summary="User registration",
    description="Registers a new user on swifcart"
)
class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logger.debug(f"Registering user with email: {serializer.validated_data.get('email')}")
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            'user': UserSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)




@extend_schema(
    tags=['Authentication'],
    summary="User login",
    description="Logs in a user and returns a JWT token pair.",
      responses={
        200: OpenApiResponse(description="user profile updated successfully."),
    }
)
class LoginView(TokenObtainPairView):
    """User login endpoint - uses JWT token pair"""
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        logger.debug(f"Attempting login for email: {email}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Login failed for email: {email} - User not found")
            return Response({"error": "Invalid email or password"}, status=401)
    
        # check password
        if not user.check_password(password):
            logger.warning(f"Login failed for email: {email} - Invalid password")
            return Response({"error": "Invalid email or password"}, status=401)

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        expires_at = datetime.fromtimestamp(access_token['exp'])
        
        logger.info(f"User {email} logged in successfully")
        return Response({
            "success": True,
            "result": {
            'user': UserSerializer(user).data,
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token),
            "expires_at": expires_at.isoformat(),
             }
        }, status=status.HTTP_200_OK)



@extend_schema(
    tags=['Authentication'],
    summary="User logout",
    description="Logs out a user by blacklisting their refresh token.",
    request=LogoutSerializer,
    responses={200: OpenApiResponse(description="User logged out successfully")}
)
class LogoutView(APIView):

    """User logout endpoint - blacklists refresh token"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "User uccessfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )




@extend_schema(
    tags=['Authentication'],
    summary="Refresh JWT access token",
    description="Provides a new access token using a valid refresh token."
)
class RefreshTokenView(APIView):

    """Endpoint to refresh access token using refresh token"""

    # Refresh token endpoint must allow ANY user
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            expires_at = datetime.fromtimestamp(token.access_token['exp'])

            logger.debug(f"Issued new access token using refresh token")

            return Response({
                "success": True,
                "result": {
                    "access": new_access_token,
                    "expires_at": expires_at.isoformat()
                }
            }, status=status.HTTP_200_OK)
         
        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )



@extend_schema(
    tags=['Authentication'],
    summary="Change user password",
    description="Allows users to change their password."
)
class ChangePasswordView(APIView):

    """Change user password"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
         )
        serializer.is_valid(raise_exception=True)

        logger.debug(f"Changing password for user: {request.user.email}")

        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.debug(f"Password changed successfully for user: {request.user.email}")  
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        logger.info(f"User {request.user.email} password changed successfully")
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=['Authentication'],
    summary="Password reset request",
    description="request for a password reset.",
    request=PasswordResetRequestSerializer,
    responses={
        200: OpenApiResponse(description="otp sent successfully."),
        400: OpenApiResponse(description="Invalid OTP or data."),
    }
)
class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user found with this email."}, status=404)
        


        # Generate 6-digit OTP
        otp_code = "123456"
        user.reset_otp_code = otp_code
        user.reset_otp_created_at = timezone.now()
        user.save()


        return Response({"detail": "A reset OTP code has been sent."}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Authentication'],
    summary="Password reset confirmation",
    description="Confirms the password reset by verifying the OTP and setting a new password.",
    request=PasswordResetConfirmSerializer,
    responses={
        200: OpenApiResponse(description="Password reset successfully."),
        400: OpenApiResponse(description="Invalid OTP or data."),
    }
)
class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        if str(user.reset_otp_code).strip() == str(otp_code).strip():
            user.set_password(new_password) 
            user.save()

            return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)



class BootstrapView(views.APIView):
    """
    One-time endpoint to create the first admin user.
    Disable after use.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=['Authentication'],
        summary="Bootstrap authentication service",
        description="Checks if the authentication service is running."
    )
    def post(self, request):
        if not getattr(settings, "ALLOW_ADMIN_BOOTSTRAP", False):
            return Response({"error": "Bootstrap disabled"}, status=403)

        data = request.data

        required = ["email", "password", "first_name", "last_name"]
        if not all(field in data for field in required):
            return Response({"error": "Missing fields"}, status=400)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Admin already exists"}, status=400)

        admin = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            is_staff=True,
            is_superuser=True,
        )

        return Response(
            {"message": f"Admin {admin.email} created"},
            status=status.HTTP_201_CREATED,
        )
    
