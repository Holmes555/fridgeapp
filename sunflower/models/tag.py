from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = ('-popularity',)

    def __repr__(self):
        return f"Tag with id {self.pk} and title {self.title}"
