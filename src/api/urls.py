from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    GroupViewSet,
    UserGroupRemoveView,
    UserGroupsView,
    UserListView,
)

router = DefaultRouter()
router.register("groups", GroupViewSet, basename="group")

urlpatterns = [
    path('', include(router.urls)),
    path("users/", UserListView.as_view()),
    path("users/<int:user_id>/groups/", UserGroupsView.as_view()),
    path("users/<int:user_id>/groups/<int:group_id>/", UserGroupRemoveView.as_view()),
]