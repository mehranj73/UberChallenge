from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)


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
