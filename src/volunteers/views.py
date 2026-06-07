# ./volunteers/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, status

from api.serializers import UserListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from volunteers.serializers import VolunteerCreateSerializer

User = get_user_model()


class VolunteerListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(
            groups__name="volunteers"
        ).distinct()


class VolunteerCreateView(generics.CreateAPIView):
    serializer_class = VolunteerCreateSerializer
    permission_classes = [IsAdminUser]