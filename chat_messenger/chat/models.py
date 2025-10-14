# from django.contrib.auth import get_user_model
# from django.db import models

# User = get_user_model()

# class Chat(models.Model):
#     name = models.CharField(max_length=255, blank=False, null=False)
#     is_group = models.BooleanField(default=False)
#     members = models.ManyToManyField(User, through='ChatMember')

# class ChatMember(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     last_read = models.DateTimeField(auto_now_add=True)

# class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def mark_as_read(self):
#         if not self.is_read:
#             self.is_read = True
#             self.save()



from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Chat(models.Model):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='ChatMember')
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"

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
    delivered = models.BooleanField(default=False)  # New field

    # def mark_as_read(self):
    #     if not self.is_read:
    #         self.is_read = True
    #         self.save()

    # def mark_as_delivered(self):
    #     if not self.delivered:
    #         self.delivered = True
    #         self.save()

    def mark_as_read(self):
        """Mark message as read (✓✓ blue ticks)."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def mark_as_delivered(self):
        """Mark message as delivered (✓✓ gray ticks)."""
        if not self.delivered:
            self.delivered = True
            self.save(update_fields=['delivered'])

    def __str__(self):
        return f"Message from {self.sender} in chat {self.chat.id}"