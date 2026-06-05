from rest_framework import serializers
from .models import MediaFile


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

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        media_file = MediaFile.objects.create(
            file=uploaded_file,
            original_name=uploaded_file.name,
            mime_type=uploaded_file.content_type,
            size=uploaded_file.size,
        )

        return media_file