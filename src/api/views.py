from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]



User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer