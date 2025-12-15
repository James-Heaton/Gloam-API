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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=50)
    character_type = models.ForeignKey(CharacterType, on_delete=models.PROTECT, related_name='characters')
    hp = models.IntegerField()
    mp = models.IntegerField()
    current_area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='characters')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Many-to-Many Join Table

class CharacterTrait(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_traits')
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE, related_name='character_traits')

    class Meta:
        unique_together = ('character', 'trait')

    def __str__(self):
        return f"{self.character.name} - {self.trait.name}"
