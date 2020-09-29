from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.contrib.auth.models import Group
from datetime import datetime


def get_user_directory_path(instance, filename):
        return f"users/{instance.username}-{instance.id}-profile-picture/{datetime.now().strftime('%Y/%H/%M-%H-%M')}/{filename}"

class User(AbstractUser):
    profile_picture = models.FileField(upload_to=get_user_directory_path, blank=True, null=True)


    @property
    def group(self):
        group = self.groups.first()
        if group:
            return group.name
        return None
