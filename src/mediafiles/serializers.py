from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import MediaFile, MediaLink, MediaType


class MediaFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = (
            "id",
            "url",
            "original_name",
            "mime_type",
            "size",
            "created_at",
        )

    def get_url(self, obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.file.url)

        return obj.file.url


class MediaUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    entity_type = serializers.CharField(required=False)
    entity_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        mime_type = uploaded_file.content_type

        media_type = (
            MediaType.IMAGE
            if mime_type.startswith("image/")
            else MediaType.VIDEO
        )

        media_file = MediaFile.objects.create(
            file=uploaded_file,
            type=media_type,
            original_name=uploaded_file.name,
            mime_type=mime_type,
            size=uploaded_file.size,
        )

        entity_type = validated_data.get("entity_type")
        entity_id = validated_data.get("entity_id")

        if entity_type and entity_id:
            MediaLink.objects.create(
                media_file=media_file,
                entity_type=entity_type,
                entity_id=entity_id,
            )

        return media_file


User = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
        )

    def get_avatar(self, obj):
        request = self.context.get("request")

        media = (
            MediaFile.objects
            .filter(
                links__entity_type="user",
                links__entity_id=obj.id,
            )
            .first()
        )

        if not media:
            return None

        if request:
            return request.build_absolute_uri(media.file.url)

        return media.file.url