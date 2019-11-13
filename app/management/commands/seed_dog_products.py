from django.core.management.base import BaseCommand, CommandError
from app import models

DOG_PRODUCTS = [
    {
        "name": "big rawhide",
        "product_type": "treat",
        "dog_size": "big dogs",
        "price": 1.55,
        "quantity": 18,
    },
    {
        "name": "peanut butter cookie",
        "product_type": "treat",
        "dog_size": "all dogs",
        "price": 0.88,
        "quantity": 33,
    },
    {
        "name": "squeaker mouse",
        "product_type": "toy",
        "dog_size": "small dogs",
        "price": 5.44,
        "quantity": 10,
    },
    {
        "name": "squeaker duck",
        "product_type": "toy",
        "dog_size": "big dogs",
        "price": 6.33,
        "quantity": 10,
    },
    {
        "name": "kong ball",
        "product_type": "toy",
        "dog_size": "all dogs",
        "price": 8.88,
        "quantity": 5,
    },
    {
        "name": "mini bone",
        "product_type": "treat",
        "dog_size": "small dogs",
        "price": 3.50,
        "quantity": 22,
    },
    {
        "name": "mega bone",
        "product_type": "treat",
        "dog_size": "big dogs",
        "price": 4.00,
        "quantity": 16,
    },
    {
        "name": "tennis ball",
        "product_type": "toy",
        "dog_size": "all dogs",
        "price": 0.99,
        "quantity": 43,
    },
    {
        "name": "premium tennis ball",
        "product_type": "toy",
        "dog_size": "all dogs",
        "price": 1.49,
        "quantity": 37,
    },
]


class Command(BaseCommand):
    help = (
        "Seeds the database with dog products based on the dog store python benchmark"
    )

    def handle(self, *args, **options):
        for dog_product in DOG_PRODUCTS:
            self.create_dog_product(dog_product)

    def create_dog_product(self, dog_product_data: dict):
        name = dog_product_data.pop("name")
        movie, created = models.DogProduct.objects.get_or_create(
            name=name, defaults=dog_product_data
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"{name} created"))
        else:
            self.stdout.write(f"{name} already exists")
