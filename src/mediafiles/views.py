from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import (
    MediaFileSerializer,
    MediaUploadSerializer,
)


class MediaFileViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = MediaUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        media_file = serializer.save()

        response_serializer = MediaFileSerializer(
            media_file,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )