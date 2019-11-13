from django.db import models

# Create your models here.
class DogProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    product_type = models.TextField()
    dog_size = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    dog_product = models.ForeignKey(DogProduct, on_delete=models.PROTECT)
    purchased_at = models.DateTimeField(auto_now=True)


class DogTag(models.Model):
    id = models.AutoField(primary_key=True)
    owner_name = models.TextField()
    dog_name = models.TextField()
    dog_birthday = models.DateField()
