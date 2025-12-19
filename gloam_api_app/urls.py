from django.urls import path
from .views.auth import register_user, login_user
from .views.character_views import character_list, character_detail
from .views.reference_views import character_type_list, trait_list, area_list

urlpatterns = [
    # Auth
    path("register", register_user, name="register"),
    path("login", login_user, name="login"),

    # Read only
    path("charactertypes", character_type_list, name="character_type_list"),
    path("traits", trait_list, name="trait_list"),
    path("areas", area_list, name="area_list"),

    # Characters
    path("characters", character_list, name="character_list"),
    path("characters/<int:character_id>", character_detail, name="character_detail")
]
