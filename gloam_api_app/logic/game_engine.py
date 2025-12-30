from ..models import Action
from .dice import roll_2d6, apply_lucky_bonus, get_outcome_tier, check_strong_proc, check_wise_proc


def check_game_status(character):
    """Check if game is over (victory or defeat)"""
    if character.hp <= 0:
        return 'defeat'
    elif character.current_area.area_number == 40:
        return 'victory'
    else:
        return 'playing'


def get_game_state(character):
    """
    Get current game state for a character
    Returns dict with area data, actions, character stats, and game status
    """
    status = check_game_status(character)

    # If game is over (victory or defeat), return minimal state
    if status != 'playing':
        return {
            'area': character.current_area,
            'actions': [],
            'character_stats': {
                'hp': character.hp if status == 'victory' else 0,
                'mp': character.mp,
                'gp': character.gp,
                'max_hp': character.max_hp,
                'max_mp': character.max_mp,
            },
            'can_use_stealthy': False,
            'game_status': status
        }

    # Normal gameplay
    actions = Action.objects.filter(area=character.current_area)
    can_use_stealthy = (
        not character.stealthy_used and
        character.character_traits.filter(trait__name='Stealthy').exists() and
        character.current_area.area_number >= 1 and
        character.current_area.area_number < 40
    )

    return {
        'area': character.current_area,
        'actions': actions,
        'character_stats': {
            'hp': character.hp,
            'mp': character.mp,
            'gp': character.gp,
            'max_hp': character.max_hp,
            'max_mp': character.max_mp,
        },
        'can_use_stealthy': can_use_stealthy,
        'game_status': 'playing'
    }


def apply_outcome(character, damage, hp_reward, mp_reward, gp_reward, new_area):
    """Apply all changes from an action outcome to the character"""

    # Apply damage
    character.hp -= damage

    # Apply rewards
    character.hp += hp_reward
    character.mp += mp_reward
    character.gp += gp_reward

    # Advance to new area
    character.current_area = new_area

    # Save once
    character.save()

    return character


def execute_safe_action(character, action):
    """Execute a safe action - simple advancement with no rolls"""

    # Apply outcome (no damage, no rewards for safe actions)
    apply_outcome(
        character=character,
        damage=0,
        hp_reward=0,
        mp_reward=0,
        gp_reward=0,
        new_area=action.destination_area
    )

    return {
        'outcome_text': action.success_text if action.success_text else "You proceed safely.",
        'lucky_procced': False,
        'strong_procced': False,
        'wise_procced': False,
        'stat_changes': {
            'hp': 0,
            'mp': 0,
            'gp': 0
        },
        'new_area_number': action.destination_area.area_number,
        'game_status': check_game_status(character)
    }


def execute_risky_action(character, action):
    """Execute a risky action with dice roll and trait checks"""

    # Roll dice
    base_roll = roll_2d6()

    # Check Lucky trait
    final_roll, lucky_procced = apply_lucky_bonus(base_roll, character)

    # Determine outcome tier
    tier = get_outcome_tier(final_roll)

    # Get outcome data based on tier
    if tier == 'failure':
        outcome_text = action.failure_text
        damage = action.failure_damage
        hp_reward = 0
        mp_reward = 0
        gp_reward = 0
        instant_death = action.instant_death_on_failure
    elif tier == 'mixed':
        outcome_text = action.mixed_text
        damage = action.mixed_damage
        hp_reward = action.mixed_hp_reward
        mp_reward = action.mixed_mp_reward
        gp_reward = action.mixed_gp_reward
        instant_death = False
    else:  # success
        outcome_text = action.success_text
        damage = 0
        hp_reward = action.success_hp_reward
        mp_reward = action.success_mp_reward
        gp_reward = action.success_gp_reward
        instant_death = False

    # Check for instant death
    if instant_death:
        character.hp = 0
        character.save()
        return {
            'outcome_text': outcome_text,
            'lucky_procced': lucky_procced,
            'strong_procced': False,
            'wise_procced': False,
            'stat_changes': {
                'hp': -character.hp,
                'mp': 0,
                'gp': 0
            },
            'new_area_number': character.current_area.area_number,
            'game_status': 'defeat'
        }

    # Check Strong trait (only if there's damage)
    strong_procced = False
    actual_damage = damage
    if damage > 0:
        strong_procced = check_strong_proc(character)
        if strong_procced:
            actual_damage = max(0, damage - 1)  # Reduce damage by 1

    # Calculate actual stat changes for response
    actual_hp_change = hp_reward - actual_damage

    # Apply outcome
    apply_outcome(
        character=character,
        damage=actual_damage,
        hp_reward=hp_reward,
        mp_reward=mp_reward,
        gp_reward=gp_reward,
        new_area=action.destination_area,
    )

    return {
        'outcome_text': outcome_text,
        'lucky_procced': lucky_procced,
        'strong_procced': strong_procced,
        'wise_procced': False,
        'stat_changes': {
            'hp': actual_hp_change,
            'mp': mp_reward,
            'gp': gp_reward
        },
        'new_area_number': action.destination_area.area_number,
        'game_status': check_game_status(character)
    }


def execute_magic_action(character, action):
    """Execute a magic action with MP cost and Wise trait check"""

    # Check if character has enough MP
    if character.mp < action.mp_cost:
        return {
            'error': 'Insufficient MP',
            'required_mp': action.mp_cost,
            'current_mp': character.mp
        }

    # Check Wise trait
    wise_procced = check_wise_proc(character)

    # Calculate MP cost (refund 1 if Wise procs)
    actual_mp_cost = max(0, action.mp_cost - (1 if wise_procced else 0))

    # Deduct MP
    character.mp -= actual_mp_cost

    # Magic actions use success_text and success rewards
    outcome_text = action.success_text if action.success_text else "Your magic carries you safely forward."
    hp_reward = action.success_hp_reward
    mp_reward = action.success_mp_reward
    gp_reward = action.success_gp_reward

    # Apply outcome (no damage from magic actions)
    apply_outcome(
        character=character,
        damage=0,
        hp_reward=hp_reward,
        mp_reward=mp_reward,
        gp_reward=gp_reward,
        new_area=action.destination_area
    )

    return {
        'outcome_text': outcome_text,
        'lucky_procced': False,
        'strong_procced': False,
        'wise_procced': wise_procced,
        'stat_changes': {
            'hp': hp_reward,
            'mp': mp_reward - actual_mp_cost,  # Net MP change
            'gp': gp_reward
        },
        'new_area_number': action.destination_area.area_number,
        'game_status': check_game_status(character)
    }


def execute_stealthy(character):
    """Execute Stealthy trait - bypass area using safe action's destination"""

    # Find safe action for current area
    safe_action = Action.objects.get(
        area=character.current_area,
        action_type='safe'
    )

    # Advance to safe action's destination
    character.current_area = safe_action.destination_area
    character.stealthy_used = True
    character.save()

    return {
        'outcome_text': "You become one with the shadows, moving through the area without detection. You have found the safest path.",
        'lucky_procced': False,
        'strong_procced': False,
        'wise_procced': False,
        'stat_changes': {
            'hp': 0,
            'mp': 0,
            'gp': 0
        },
        'new_area_number': safe_action.destination_area.area_number,
        'game_status': check_game_status(character)
    }


def execute_action(character, action_id=None, use_stealthy=False):
    """
    Main game loop handler - orchestrates all action execution
    Either action_id OR use_stealthy must be provided
    """

    if use_stealthy:
        return execute_stealthy(character)

    if not action_id:
        return {'error': 'No action specified'}

    # Get the action
    try:
        action = Action.objects.get(id=action_id, area=character.current_area)
    except Action.DoesNotExist:
        return {'error': 'Invalid action for current area'}

    # Execute based on action type
    if action.action_type == 'safe':
        return execute_safe_action(character, action)
    elif action.action_type == 'risky':
        return execute_risky_action(character, action)
    elif action.action_type == 'magic':
        return execute_magic_action(character, action)
    else:
        return {'error': 'Unknown action type'}
