from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import CharacterType, Trait, Area
from ..serializers import CharacterTypeSerializer, TraitSerializer, AreaSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def character_type_list(request):
    """Get all character types"""
    character_types = CharacterType.objects.all()
    serializer = CharacterTypeSerializer(character_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trait_list(request):
    """Get all traits"""
    traits = Trait.objects.all()
    serializer = TraitSerializer(traits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def area_list(request):
    """Get all areas"""
    areas = Area.objects.all()
    serializer = AreaSerializer(areas, many=True)
    return Response(serializer.data)
