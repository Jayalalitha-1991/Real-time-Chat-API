from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Chat(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='ChatMember')

class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)