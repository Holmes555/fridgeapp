from django.db import models

from sunflower.models import CustomUser
from sunflower.models.recipe import Recipe


class CookBook(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __repr__(self):
        return (f"CookBook with id {self.pk} and "
                f"user id {self.author.pk}")
