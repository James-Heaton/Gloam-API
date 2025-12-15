from django.contrib import admin
from .models import Area, CharacterType, Trait, Character, CharacterTrait

admin.site.register(Area)
admin.site.register(CharacterType)
admin.site.register(Trait)
admin.site.register(Character)
admin.site.register(CharacterTrait)
