from django.db import models

from fridgeapp.models import CustomUser
from fridgeapp.models.recipe import Recipe


class RecipeComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    content = models.TextField()
    photo = models.ImageField(upload_to="files/media/", blank=True, default="")
    publish_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-publish_date",)

    def __repr__(self):
        return (
            f"Comment with id {self.pk}, recipe id {self.recipe_id}"
            f" and author id {self.author.pk}"
        )
