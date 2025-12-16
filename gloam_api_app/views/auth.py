from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Handle User Registration"""

    # Get data from request
    username = request.data.get("username")
    password = request.data.get("password")

    # Validate fields
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if username exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user
    user = User.objects.create_user(username=username, password=password)

    # Create token
    token = Token.objects.create(user=user)

    # Return success response with token
    return Response(
        {"token": token.key, "user_id": user.id, "username": user.username},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Handle User Login"""

    # Get credentials from request
    username = request.data.get("username")
    password = request.data.get("password")

    # Validate fields
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Authenticate the user
    user = authenticate(username=username, password=password)

    # Check if authentication was successful
    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Get or create token for user
    token, created = Token.objects.get_or_create(user=user)

    # Return success response with token
    return Response(
        {"token": token.key, "user_id": user.id, "username": user.username},
        status=status.HTTP_200_OK,
    )
