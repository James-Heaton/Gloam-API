from django.contrib import admin
from .models import Area, Action, CharacterType, Trait, Character, CharacterTrait


class CharacterAdmin(admin.ModelAdmin):
    fields = ["user", "name", "character_type", "current_area", "is_active", "hp", "mp", "gp", "stealthy_used"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Only for new objects
            form.base_fields["hp"].required = False
            form.base_fields["mp"].required = False
            form.base_fields["current_area"].required = False
            form.base_fields["gp"].required = False
            form.base_fields["stealthy_used"].required = False
        return form


admin.site.register(Area)
admin.site.register(CharacterType)
admin.site.register(Trait)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterTrait)
admin.site.register(Action)
