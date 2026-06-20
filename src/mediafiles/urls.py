# src/mediafiles/urls.py

from rest_framework.routers import DefaultRouter

from .views import MediaFileViewSet

router = DefaultRouter()

router.register(
    "media",
    MediaFileViewSet,
    basename="media"
)

urlpatterns = router.urls