from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __repr__(self):
        return f"User with id {self.pk} and login {self.username}"
