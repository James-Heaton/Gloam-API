from django.db import models
from django.contrib.auth.models import User

# Read only Models


class Area(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


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
    current_area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="characters", null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

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
        """Reset character HP/MP to max values"""
        self.hp = self.character_type.max_hp
        self.mp = self.character_type.max_mp
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
