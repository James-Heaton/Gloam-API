from rest_framework import serializers
from ..models import Action, Area


class ActionSerializer(serializers.ModelSerializer):
    """
    Serializer for Action model.
    CRITICAL: Hides outcome details (failure_text, damage, etc.)
    Players should not see what will happen before they choose!
    """

    class Meta:
        model = Action
        fields = ["id", "action_text", "action_type", "mp_cost", "order"]
        # NOT including:
        # - destination_area
        # - failure_text, mixed_text, success_text
        # - damage values
        # - reward values
        # - instant_death_on_failure


class AreaWithActionsSerializer(serializers.ModelSerializer):
    """
    Serializer for Area with nested actions.
    Used in game state responses.
    """

    actions = ActionSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ["area_number", "name", "description", "actions"]


class GameStateSerializer(serializers.Serializer):
    """
    Comprehensive game state response.
    This is what GET /api/game/state/ returns.
    """

    area = AreaWithActionsSerializer(read_only=True)
    character_stats = serializers.DictField(read_only=True)
    can_use_stealthy = serializers.BooleanField(read_only=True)
    game_status = serializers.CharField(read_only=True)


class ActionResultSerializer(serializers.Serializer):
    """
    Response after executing an action.
    This is what POST /api/game/action/ returns.
    """

    outcome_text = serializers.CharField(read_only=True)
    lucky_procced = serializers.BooleanField(read_only=True)
    strong_procced = serializers.BooleanField(read_only=True)
    wise_procced = serializers.BooleanField(read_only=True)
    stat_changes = serializers.DictField(read_only=True)
    new_area_number = serializers.IntegerField(read_only=True)
    game_status = serializers.CharField(read_only=True)

    # Optional error field
