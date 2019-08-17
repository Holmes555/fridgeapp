from django.db import models

from fridgeapp.models import CustomUser
from fridgeapp.models.product import Product


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.FloatField(default=0)
    measure = models.CharField(max_length=35)

    def __repr__(self):
        return f"Ingredient with id {self.pk} product id {self.product.pk}"
