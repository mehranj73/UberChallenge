from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.contrib.auth.models import Group


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, password, group=None,**kwargs):
        user = self.model(
            username=username,
            **kwargs
        )
        user.set_password(password)
        # if group:
        #     print(Group.objects.all())
        #     driver_group = Group.objects.get(name="driver")
        #     driver_group.user_set.add(user)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    pass
    objects = UserManager()
