# from rest_framework import generics, permissions
# from .models import Chat, Message
# from .serializers import ChatSerializer, MessageSerializer
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView


# class ChatListCreateView(APIView):

#     def get(self, request):
#         chats = Chat.objects.all()
#         serializer = ChatSerializer(chats, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ChatSerializer(data=request.data)
#         if serializer.is_valid():
#             chat = serializer.save()
#             # Optional: Add the requesting user to the chat as a member
#             user = request.user if request.user and request.user.is_authenticated else None
#             if user:
#                 chat.members.add(user)
#             return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MessageListCreateView(APIView):

#     def get(self, request, chat_id):
#         messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')

#         # If user is authenticated, mark unread messages (sent by others) as read
#         if request.user.is_authenticated:
#             unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
#             for message in unread_messages:
#                 message.mark_as_read()

#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, chat_id):
#         data = request.data.copy()
#         data['chat'] = chat_id

#         user = request.user if request.user and request.user.is_authenticated else None
#         if user:
#             data['sender'] = user.id
#         else:
#             return Response({'detail': 'Authentication required to send messages.'}, status=status.HTTP_401_UNAUTHORIZED)

#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             message = serializer.save(sender=user)
#             return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.views import APIView
from .utils import is_user_online, set_user_online
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Chat
# from .serializers import ChatSerializer


# class ChatListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Only show chats that the user is a member of
#         chats = Chat.objects.filter(members=request.user)
#         serializer = ChatSerializer(chats, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         user = request.user

#         # Check if this user has already created a chat
#         existing_chat = Chat.objects.filter(members=user).exists()
#         if existing_chat:
#             return Response(
#                 {"error": "You have already created a chat."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Otherwise, create a new chat
#         serializer = ChatSerializer(data=request.data)
#         if serializer.is_valid():
#             chat = serializer.save()
#             chat.members.add(user)
#             return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChatListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only show chats that the user is a member of
        chats = Chat.objects.filter(members=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        chat_name = request.data.get("name")  # assuming your Chat model has a 'name' field

        if not chat_name:
            return Response(
                {"error": "Chat name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Check if a chat with the same name already exists
        if Chat.objects.filter(name__iexact=chat_name).exists():
            return Response(
                {"error": f"A chat with the name '{chat_name}' already exists. Please choose a different name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Check if this user already created/joined a chat
        if Chat.objects.filter(members=user).exists():
            return Response(
                {"error": "You have already created a chat."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Otherwise, create a new chat
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            chat.members.add(user)
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404

class MessageListCreateView(APIView):
    # def get(self, request, chat_id):
    #     messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')

    #     if request.user.is_authenticated:
    #         set_user_online(request.user.id)  # Mark user online
    #         unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
    #         for message in unread_messages:
    #             message.mark_as_read()

    #     serializer = MessageSerializer(messages, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, chat_id):
        # Validate chat existence
        chat = get_object_or_404(Chat, id=chat_id)
        messages = Message.objects.filter(chat=chat).order_by('timestamp')

        if request.user.is_authenticated:
            # Mark user as online
            set_user_online(request.user.id)

            # Get messages not sent by this user (received messages)
            received_messages = messages.exclude(sender=request.user)

            # Step 1: Mark all received messages as delivered
            for message in received_messages:
                message.mark_as_delivered()

            # Step 2: Mark unread messages as read
            unread_messages = received_messages.filter(is_read=False)
            for message in unread_messages:
                message.mark_as_read()

        # Serialize all messages (so frontend can show ticks correctly)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





    def post(self, request, chat_id):
        data = request.data.copy()
        data['chat'] = chat_id

        user = request.user if request.user and request.user.is_authenticated else None
        if not user:
            return Response({'detail': 'Authentication required to send messages.'}, status=status.HTTP_401_UNAUTHORIZED)

        data['sender'] = user.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save(sender=user)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
