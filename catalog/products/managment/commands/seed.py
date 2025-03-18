import random

from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Product, Category


class Command(BaseCommand):
    help = "Generates text data for databases"

    def handle(self, *args, **options):
        fake = Faker()
        categories = ["Computers", "Phones", "Tablets", "Laptops", "VRs"]
        categories_objects = [
            Category.objects.get_or_create(name=c) for c in categories
        ]

        Product.objects.all().delete()

        for _ in range(50):
            Product.objects.create(
                name=fake.word().capitalize(),
                category=random.choice(categories, nomenclature=fake.unique.uuid4()),
                description=fake.text(max_nb_chars=100),
                price=random.randint(1, 100),
                discount=random.randint(0, 51),
                stock=random.randint(1, 1000),
                available=random.choice([True, False]),
                rating=round(random.uniform(0.1, 5.0), 1),
                attributes={
                    "color": fake.color_name(),
                },
            )

        self.stdout.write(self.style.SUCCESS("CREATED 50 CHELICKS"))
