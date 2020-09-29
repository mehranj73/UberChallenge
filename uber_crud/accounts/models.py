from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.contrib.auth.models import Group


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, password,**kwargs):
        user = self.model(
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    pass
    objects = UserManager()

    @property
    def group(self):
        group = self.groups.first()
        if group:
            return group.name
        return None
