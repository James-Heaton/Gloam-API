from django.db import models
from django.contrib.auth.models import User

# Read only Models


class Area(models.Model):
    area_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['area_number']

    def __str__(self):
        return f"Area {self.area_number}: {self.name}"


class Action(models.Model):
    ACTION_TYPES = [
        ('safe', 'Safe'),
        ('risky', 'Risky'),
        ('magic', 'Magic'),
    ]

    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='actions')
    action_text = models.TextField()
    action_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    destination_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='destination_for')
    order = models.IntegerField()  # 1, 2, 3, or 4

    # For magic actions
    mp_cost = models.IntegerField(default=0)

    # For risky actions - outcome texts
    failure_text = models.TextField(blank=True)
    failure_damage = models.IntegerField(default=0)
    mixed_text = models.TextField(blank=True)
    mixed_damage = models.IntegerField(default=0)
    success_text = models.TextField(blank=True)

    # For risky actions - mixed outcome rewards
    mixed_hp_reward = models.IntegerField(default=0)
    mixed_mp_reward = models.IntegerField(default=0)
    mixed_gp_reward = models.IntegerField(default=0)

    # For risky actions - success outcome rewards
    success_hp_reward = models.IntegerField(default=0)
    success_mp_reward = models.IntegerField(default=0)
    success_gp_reward = models.IntegerField(default=0)

    # Special flags
    instant_death_on_failure = models.BooleanField(default=False)


    class Meta:
        ordering = ['area', 'order']

    def __str__(self):
        return f"{self.area.name} - Action {self.order} ({self.action_type})"


class CharacterType(models.Model):
    name = models.CharField(max_length=50)
    max_hp = models.IntegerField()
    max_mp = models.IntegerField()

    def __str__(self):
        return self.name


class Trait(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


# CRUD Model


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=50)
    character_type = models.ForeignKey(
        CharacterType, on_delete=models.PROTECT, related_name="characters"
    )
    hp = models.IntegerField()
    mp = models.IntegerField()
    gp = models.IntegerField(default=0)
    current_area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="characters", null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    stealthy_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Set HP, MP, and starting area on creation if not provided"""
        is_new = not self.pk  # Check if this is a new character

        if is_new:
            if not self.hp:
                self.hp = self.character_type.max_hp
            if not self.mp:
                self.mp = self.character_type.max_mp
            if not self.current_area_id:
                self.current_area_id = 1

        super().save(*args, **kwargs)

        # If this is a new character, automatically set it as active
        if is_new:
            self.set_active()

    def set_active(self):
        """Set this character as active, deactivating all others for this user"""
        # Deactivate all other characters for this user
        Character.objects.filter(user=self.user).exclude(pk=self.pk).update(is_active=False)
        # Activate this character
        self.is_active = True
        self.save(update_fields=['is_active'])  # Only update is_active to avoid recursion

    @property
    def max_hp(self):
        """Get max HP from character type"""
        return self.character_type.max_hp

    @property
    def max_mp(self):
        """Get max MP from character type"""
        return self.character_type.max_mp

    def reset_to_defaults(self):
        """Reset character to starting state for new game"""
        self.hp = self.character_type.max_hp
        self.mp = self.character_type.max_mp
        self.gp = 0
        self.current_area_id = 1
        self.stealthy_used = False
        self.save()

    def __str__(self):
        return self.name


# Many-to-Many Join Table


class CharacterTrait(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_traits"
    )
    trait = models.ForeignKey(
        Trait, on_delete=models.CASCADE, related_name="character_traits"
    )

    class Meta:
        unique_together = ("character", "trait")

    def __str__(self):
        return f"{self.character.name} - {self.trait.name}"
