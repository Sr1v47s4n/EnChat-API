from .models import User, DEFAULT_PROFILE_PICS
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    profile_picture = request.data.get("profile_picture")
    if email is None or password is None or username is None:
        return Response({"error": "Please provide all fields"}, status=400)
    if email:
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email"}, status=400)
    #vaildate pass
    if len(password) < 8 or len(password) > 16 or password.isalnum() or password.isalpha() or password.isdigit() or password.islower() or password.isupper():
        return Response({"error": "Password must be 8-16 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character"}, status=400)
    
    if profile_picture not in DEFAULT_PROFILE_PICS:
        profile_picture = DEFAULT_PROFILE_PICS[0]  # Default image

    if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
        return Response({"error": "Username or email already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    return Response({"message": "User registered successfully"}, status=201)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_profile_pictures(request):
    return Response({"profile_pictures": DEFAULT_PROFILE_PICS})


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if user is None:
        return Response({"error": "Invalid email or password"}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        , status=200
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({"message": "Logged out successfully"})
