from django.db import models

from sunflower.models import CustomUser


class CookBookRelation(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cookbook_id = models.IntegerField()
    subcookbook_id = models.IntegerField()

    def __repr__(self):
        return (f"CookBookRelation with id {self.pk}, "
                f"cookbook id {self.cookbook_id} and subcookbook id "
                f"{self.subcookbook_id}")
