from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Character
from ..serializers import CharacterSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def character_list(request):
    """Get all characters for the auth user or Create new character"""

    if request.method == 'GET':
        # Get all characters for the authenticated user
        characters = Character.objects.filter(user=request.user)
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new character
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = CharacterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def character_detail(request, character_id):
    """Get or update a single character by ID"""
    try:
        # Get character only if it belongs to auth user
        character = Character.objects.get(pk=character_id, user=request.user)
    except Character.DoesNotExist:
        return Response(
            {'error': "Character not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the character
        serializer = CharacterSerializer(character, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the character
        character.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_active_character(request, character_id):
    """Set a character as the active character for the authenticated user"""
    try:
        # Get character only if it belongs to auth user
        character = Character.objects.get(pk=character_id, user=request.user)
    except Character.DoesNotExist:
        return Response(
            {'error': "Character not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Set this character as active
    character.set_active()

    serializer = CharacterSerializer(character)
    return Response(serializer.data)
