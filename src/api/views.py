from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GroupSerializer, UserListSerializer, UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


User = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class UserGroupsView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = GroupSerializer(user.groups.all(), many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        group_ids = request.data.get("group_ids")
        if not isinstance(group_ids, list) or not group_ids:
            return Response(
                {"detail": "Field 'group_ids' is required and must be a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        groups = Group.objects.filter(id__in=group_ids)
        user.groups.add(*groups)

        serializer = GroupSerializer(user.groups.all(), many=True)
        return Response(serializer.data)


class UserGroupRemoveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, user_id, group_id):
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)

        user.groups.remove(group)

        return Response(status=status.HTTP_204_NO_CONTENT)
