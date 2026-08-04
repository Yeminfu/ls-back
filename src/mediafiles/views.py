from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import MediaFile
from .pagination import MediaPageNumberPagination
from .serializers import (
    MediaFileSerializer,
    MediaUploadSerializer,
)


class MediaFileViewSet(viewsets.ViewSet):
    serializer_class = MediaFileSerializer
    pagination_class = MediaPageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset,
            self.request,
            view=self,
        )

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "entity_type",
                type=str,
                required=False,
                description="Type of the linked entity (e.g. 'user').",
            ),
            OpenApiParameter(
                "entity_id",
                type=int,
                required=False,
                description="ID of the linked entity.",
            ),
        ],
    )
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MediaFileSerializer(
                page,
                many=True,
                context={"request": request},
            )
            return self.get_paginated_response(serializer.data)

        serializer = MediaFileSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)