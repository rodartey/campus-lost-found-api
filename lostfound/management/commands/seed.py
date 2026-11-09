import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from lostfound.models import Claim, Comment, Item

User = get_user_model()

USERNAMES = ["ama", "kofi", "esi", "yaw", "abena"]

ITEMS = [
    ("Black backpack", "Black Jansport with a laptop sleeve inside", "Main Library", "lost"),
    ("Blue water bottle", "Steel bottle with a KNUST sticker", "Engineering Block", "found"),
    ("Student ID card", "ID card, name partly worn off", "Brunei Hall", "found"),
    ("Samsung phone", "Dark blue phone with a cracked screen", "Commercial Area", "lost"),
    ("Calculator", "Casio fx-991 scientific calculator", "Lecture Theatre 3", "found"),
    ("Car keys", "Toyota key with a red tag", "Unity Hall", "lost"),
    ("Umbrella", "Large black umbrella", "Science Block", "found"),
    ("Earbuds case", "White wireless earbuds case", "Cafeteria", "lost"),
    ("Textbook", "Database Systems textbook with notes inside", "Main Library", "claimed"),
    ("Wallet", "Brown leather wallet with some cash", "Bus stop", "returned"),
    ("Jacket", "Grey hoodie, size L", "Sports Complex", "found"),
    ("Flash drive", "16GB silver flash drive", "ICT Lab", "lost"),
]

CLAIM_MESSAGES = [
    "I think this is mine, I lost it yesterday.",
    "This looks like my item, I can describe what is inside.",
    "I was here this morning and left it behind.",
]

COMMENTS = [
    "Has anyone seen this around?",
    "I think I saw this near the entrance earlier.",
    "I have handed it in at the security office.",
    "Still looking for the owner.",
]


class Command(BaseCommand):
    help = "Seed the database with demo users, items, claims and comments."

    def handle(self, *args, **options):
        Comment.objects.all().delete()
        Claim.objects.all().delete()
        Item.objects.all().delete()

        users = []
        for name in USERNAMES:
            user, created = User.objects.get_or_create(username=name)
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        for title, description, location, status in ITEMS:
            item = Item.objects.create(
                title=title,
                description=description,
                location=location,
                status=status,
                reported_by=random.choice(users),
            )
            item.watchers.set(random.sample(users, k=random.randint(0, 3)))

            for _ in range(random.randint(0, 2)):
                Claim.objects.create(
                    item=item,
                    claimant=random.choice(users),
                    message=random.choice(CLAIM_MESSAGES),
                    status=random.choice(Claim.Status.values),
                )
            for _ in range(random.randint(0, 3)):
                Comment.objects.create(
                    item=item,
                    author=random.choice(users),
                    text=random.choice(COMMENTS),
                )

        self.stdout.write(self.style.SUCCESS("Seeded users, items, claims and comments."))