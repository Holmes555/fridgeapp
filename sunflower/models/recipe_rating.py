from django.db import models


class RecipeRating(models.Model):
    rating = models.FloatField(default=0)
    mark_count = models.IntegerField(default=0)
    mark_sum = models.FloatField(default=0)

    def __repr__(self):
        return (f"RecipeRating with id {self.pk} "
                f"and rating {self.rating}")
