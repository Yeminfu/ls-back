import uuid

from django.db import models


class MediaType(models.TextChoices):
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"


class MediaFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
    )

    file = models.FileField(
        upload_to="media/%Y/%m/"
    )

    original_name = models.CharField(
        max_length=255
    )

    mime_type = models.CharField(
        max_length=100
    )

    size = models.BigIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "media_files"


class MediaLink(models.Model):
    media_file = models.ForeignKey(
        "mediafiles.MediaFile",
        on_delete=models.CASCADE,
        related_name="links",
    )

    entity_type = models.CharField(
        max_length=100,
    )

    entity_id = models.BigIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "media_links"
        indexes = [
            models.Index(
                fields=["entity_type", "entity_id"]
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "media_file",
                    "entity_type",
                    "entity_id",
                ],
                name="unique_media_link",
            )
        ]