from rest_framework import generics, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ChatListCreateView(APIView):

    def get(self, request):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            # Optional: Add the requesting user to the chat as a member
            user = request.user if request.user and request.user.is_authenticated else None
            if user:
                chat.members.add(user)
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageListCreateView(APIView):

    def get(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, chat_id):
        data = request.data.copy()
        data['chat'] = chat_id

        user = request.user if request.user and request.user.is_authenticated else None
        if user:
            data['sender'] = user.id
        else:
            return Response({'detail': 'Authentication required to send messages.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save(sender=user)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
