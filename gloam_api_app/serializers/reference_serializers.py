from rest_framework import serializers
from ..models import CharacterType, Trait, Area


class CharacterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterType
        fields = ["id", "name", "max_hp", "max_mp"]


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = ["id", "name", "description"]


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["id", "area_number", "name", "description"]
