from django.contrib.auth.models import AbstractUser
from django.db import models


class DjangoUser(AbstractUser):
    tg_username = models.TextField("tg_username")
    tg_name = models.TextField("tg_name")

    def save(self, *args, **kwargs):
        # Skip saving into DB
        ...

