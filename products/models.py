# # Products models.py
from django.db import models
from pyuploadcare.dj.models import ImageField
# Create your models here.


class ProductType(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Colour(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


# Main Product Model
class Product(models.Model):
    name = models.CharField(blank=False, max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    image = ImageField(blank=True, manual_crop="")
    price = models.DecimalField(
        blank=False, max_digits=19, decimal_places=2)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    length = models.FloatField(blank=False)
    desc = models.TextField(blank=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return self.name
