from django.contrib import admin
from app.models import DogProduct, Purchase, DogTag, Review

# Register your models here.
models = [DogProduct, Purchase, DogTag, Review]
for model in models:
    admin.site.register(model)
