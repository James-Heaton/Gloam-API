from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Character
from ..serializers.game_serializers import GameStateSerializer, ActionResultSerializer
from ..logic.game_engine import get_game_state, execute_action


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_state(request):
    """
    Get current game state for the authenticated user's active character.
    Returns area, actions, character stats, and game status.
    """
    try:
        # Get the active character for this user
        character = Character.objects.get(user=request.user, is_active=True)
    except Character.DoesNotExist:
        return Response(
            {'error': 'No active character found. Please activate a character first.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Get game state from game engine
    state = get_game_state(character)

    # Serialize and return
    serializer = GameStateSerializer(state)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_game_action(request):
    """
    Execute an action for the authenticated user's active character.
    
    Request body:
    {
        "action_id": 5,  // Optional - ID of action to execute
        "use_stealthy": false  // Optional - true to use Stealthy trait
    }
    
    Returns action result with outcome text, trait procs, stat changes, etc.
    """
    try:
        character = Character.objects.get(user=request.user, is_active=True)
    except Character.DoesNotExist:
        return Response(
            {'error': 'No active character found. Please activate a character first.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Get parameters from request
    action_id = request.data.get('action_id')
    use_stealthy = request.data.get('use_stealthy', False)

    # Execute the action
    result = execute_action(
        character=character,
        action_id=action_id,
        use_stealthy=use_stealthy
    )

    # Check for errors in result
    if 'error' in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    # Serialize and return
    serializer = ActionResultSerializer(result)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_game(request):
    """
    Reset the authenticated user's active character to starting state.
    Calls character.reset_to_defaults() to reset HP, MP, GP, area, and stealthy_used.
    """
    try:
        character = Character.objects.get(user=request.user, is_active=True)
    except Character.DoesNotExist:
        return Response(
            {'error': 'No active character found. Please activate a character first.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Reset the character
    character.reset_to_defaults()

    return Response({
        'message': 'Character reset to starting state.',
        'character': {
            'name': character.name,
            'hp': character.hp,
            'mp': character.mp,
            'gp': character.gp,
            'area': character.current_area.area_number
        }
    })
