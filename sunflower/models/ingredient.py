from django.db import models

from sunflower.models import CustomUser
from sunflower.models.product import Product


class Ingredient(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.FloatField(default=0)
    measure = models.CharField(max_length=35)

    def __repr__(self):
        return f"Ingredient with id {self.pk} product id {self.product.pk}"
