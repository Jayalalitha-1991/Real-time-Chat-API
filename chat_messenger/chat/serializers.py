# from rest_framework import serializers
# from .models import Chat, Message

# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.StringRelatedField()

#     class Meta:
#         model = Message
#         fields = ['id', 'chat', 'sender', 'content', 'timestamp', 'is_read']

# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = ['id', 'name', 'is_group']





from rest_framework import serializers
from .models import Chat, Message
from .utils import is_user_online

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'is_group']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp', 'is_read', 'status']

    def get_status(self, obj):
        if obj.is_read:
            return "blue_double_tick"
        elif hasattr(obj, 'delivered') and obj.delivered:
            return "double_tick"
        else:
            chat_members = obj.chat.members.exclude(id=obj.sender.id)
            for member in chat_members:
                if is_user_online(member.id):
                    if hasattr(obj, 'mark_as_delivered'):
                        obj.mark_as_delivered()
                    return "double_tick"
            return "single_tick"

