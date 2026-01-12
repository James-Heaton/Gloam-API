import random


def roll_2d6():
    """Roll 2d6 and return the sum (2-12)"""
    return random.randint(1, 6) + random.randint(1, 6)


def check_lucky_proc(character):
    """
    Check if Lucky trait procs (35% chance)
    Returns True if character has Lucky trait AND it procs
    """
    if not character:
        return False

    # Check if character has Lucky trait
    has_lucky = character.character_traits.filter(trait__name='Lucky').exists()

    if not has_lucky:
        return False

    # 35% chance to proc
    return random.random() < 0.35


def check_strong_proc(character):
    """
    Check if Strong trait procs (25% chance)
    Returns True if character has Strong trait AND it procs
    """
    if not character:
        return False

    has_strong = character.character_traits.filter(trait__name='Strong').exists()

    if not has_strong:
        return False

    # 25% chance to proc
    return random.random() < 0.25


def check_wise_proc(character):
    """
    Check if Wise trait procs (25% chance)
    Returns True if character has Wise trait AND it procs
    """
    if not character:
        return False

    has_wise = character.character_traits.filter(trait__name='Wise').exists()

    if not has_wise:
        return False

    # 25% chance to proc
    return random.random() < 0.25


def apply_lucky_bonus(base_roll, character):
    """
    Check for Lucky proc and apply +1 bonus if it happens
    Returns (final_roll, lucky_procced)
    """
    lucky_procced = check_lucky_proc(character)

    if lucky_procced:
        return (base_roll + 1, True)
    else:
        return (base_roll, False)


def get_outcome_tier(roll):
    """
    Convert 2d6 roll into outcome tier
    1-6: failure
    7-9: mixed
    10-12: success
    """
    if roll <= 6:
        return 'failure'
    elif roll <= 9:
        return 'mixed'
    else:
        return 'success'
