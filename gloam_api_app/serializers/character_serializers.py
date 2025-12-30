from rest_framework import serializers
from ..models import Character, CharacterType, Trait, CharacterTrait


class CharacterSerializer(serializers.ModelSerializer):
    # Read-only fields that come from relationships
    character_type_name = serializers.CharField(
        source="character_type.name", read_only=True
    )
    max_hp = serializers.IntegerField(read_only=True)
    max_mp = serializers.IntegerField(read_only=True)

    # Write-only field for accepting trait IDs
    trait_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True,
        min_length=2,
        max_length=2,
    )

    # Read-only field for returning trait details
    traits = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = [
            "id",
            "user",
            "name",
            "character_type",
            "character_type_name",
            "hp",
            "mp",
            "gp",
            "max_hp",
            "max_mp",
            "current_area",
            "is_active",
            "stealthy_used",
            "trait_ids",
            "traits",
        ]
        read_only_fields = [
            "id",
            "hp",
            "mp",
            "gp",
            "current_area",
            "is_active",
            "stealthy_used",
        ]
        extra_kwargs = {
            "user": {"write_only": True},
        }

    def get_traits(self, obj):
        """Return list of traits for this character"""
        traits = Trait.objects.filter(character_traits__character=obj)
        return [
            {"id": trait.id, "name": trait.name, "description": trait.description}
            for trait in traits
        ]

    def create(self, validated_data):
        """Handle character creation with traits"""
        # Extract trait_ids from validated data
        trait_ids = validated_data.pop("trait_ids", [])

        # Create character (starting hp, mp, and current_area set by model's save method)
        character = Character.objects.create(**validated_data)

        # Add traits to character
        for trait_id in trait_ids:
            CharacterTrait.objects.create(character=character, trait_id=trait_id)

        return character

    def update(self, instance, validated_data):
        """Handle character updates with traits"""
        # Extract trait_ids if provided

        trait_ids = validated_data.pop("trait_ids", None)

        character_changed = False

        # Update basic fields
        for attr, value in validated_data.items():
            if attr not in ["user", "name"]:
                if getattr(instance, attr) != value:
                    character_changed = True
                    setattr(instance, attr, value)

        # If character type or traits changed, reset to defaults
        if character_changed or trait_ids is not None:
            instance.hp = instance.character_type.max_hp
            instance.mp = instance.character_type.max_mp
            instance.current_area_id = 1

        # Update traits if provided
        if trait_ids is not None:
            # Remove existing traits
            CharacterTrait.objects.filter(character=instance).delete()
            # Add new traits
            for trait_id in trait_ids:
                CharacterTrait.objects.create(character=instance, trait_id=trait_id)

        return instance
