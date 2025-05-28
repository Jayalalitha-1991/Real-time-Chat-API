from django.db import models

# Create your models here.
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_online = models.BooleanField(default=False)
    # Add profile_pic or other fields as needed