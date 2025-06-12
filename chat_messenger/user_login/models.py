from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    security_question = models.CharField(max_length=255, null=True, blank=True)
    security_answer = models.CharField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.username
