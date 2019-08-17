from django.db import models

from fridgeapp.models import CustomUser


class RecipeStep(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.URLField(max_length=128, blank=True, default="")
    step_number = models.IntegerField(default=0)

    class Meta:
        ordering = ("step_number",)

    def __repr__(self):
        return f"Recipe step with id {self.pk}, and order {self.step_number}"
