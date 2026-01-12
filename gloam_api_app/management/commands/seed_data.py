from django.core.management.base import BaseCommand
from gloam_api_app.models import Area, CharacterType, Trait


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Seed CharacterTypes
        self.stdout.write("Creating CharacterTypes...")
        CharacterType.objects.get_or_create(
            name="Fighter", defaults={"max_hp": 12, "max_mp": 8}
        )
        CharacterType.objects.get_or_create(
            name="Ranger", defaults={"max_hp": 10, "max_mp": 10}
        )
        CharacterType.objects.get_or_create(
            name="Wizard", defaults={"max_hp": 8, "max_mp": 12}
        )

        # Seed Traits
        self.stdout.write("Creating Traits...")
        Trait.objects.get_or_create(
            name="Strong", defaults={"description": "Chance to ignore harm"}
        )
        Trait.objects.get_or_create(
            name="Wise", defaults={"description": "Chance to ignore MP cost"}
        )
        Trait.objects.get_or_create(
            name="Lucky",
            defaults={"description": "Chance to improve your odds of success"},
        )
        Trait.objects.get_or_create(
            name="Stealthy",
            defaults={
                "description": "Automatically find the safest route through an area"
            },
        )

        # Seed Areas
        self.stdout.write("Creating Areas...")
        Area.objects.get_or_create(
            name="Entrance Hall",
            defaults={
                "description": "You enter a vast entrance hall, its vaulted ceiling lost in shadow high above. Moonlight streams through shattered stained glass windows, casting fractured colors across the cracked marble floor. The air is cold and still, carrying the faint scent of old stone and something else — something sweet and rotten that makes your stomach turn. A staircase curves upward to your left, its stone balustrade carved with leering faces that seem to follow your every move. Straight ahead, a heavy iron-banded door stands slightly ajar, revealing only darkness beyond. At the center of the hall, in the light of the broken windows, stands a stone altar covered in ancient dust and dried wax."
            },
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
