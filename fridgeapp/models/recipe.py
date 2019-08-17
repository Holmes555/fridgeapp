from django.db import models

from fridgeapp.models import CustomUser
from fridgeapp.models.ingredient import Ingredient
from fridgeapp.models.recipe_rating import RecipeRating
from fridgeapp.models.recipe_step import RecipeStep
from fridgeapp.models.tag import Tag


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.ForeignKey(RecipeRating, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)
    recipe_steps = models.ManyToManyField(RecipeStep)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.URLField(max_length=128, blank=True, default="")
    publish_date = models.DateField(auto_now_add=True)
    cooking_time = models.IntegerField(default=0, help_text="in minutes")
    person_count = models.IntegerField(default=0)
    steps_count = models.IntegerField(default=0)

    class Meta:
        ordering = ("-rating__rating", "-publish_date")

    def __repr__(self):
        return (
            f"Recipe with id {self.pk}, title {self.title} and "
            f"author id {self.author.pk}"
        )
