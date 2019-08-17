from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __repr__(self):
        return f"Product with id {self.pk} and name {self.name}"
