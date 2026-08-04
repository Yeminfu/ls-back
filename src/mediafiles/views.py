from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import MediaFile
from .serializers import (
    MediaFileSerializer,
    MediaUploadSerializer,
)


class MediaFileViewSet(viewsets.ViewSet):
    serializer_class = MediaFileSerializer

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

    def retrieve(self, request, pk=None):
        media_file = get_object_or_404(MediaFile, pk=pk)
        serializer = MediaFileSerializer(
            media_file,
            context={"request": request},
        )
        return Response(serializer.data)

    def list(self, request):
        entity_type = request.query_params.get("entity_type")
        entity_id = request.query_params.get("entity_id")

        if bool(entity_type) != bool(entity_id):
            return Response(
                {
                    "detail": (
                        "entity_type and entity_id must be provided together."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if entity_type and entity_id:
            queryset = MediaFile.objects.filter(
                links__entity_type=entity_type,
                links__entity_id=entity_id,
            )
        else:
            queryset = MediaFile.objects.all()

        serializer = MediaFileSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)