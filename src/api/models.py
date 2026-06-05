from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.ForeignKey(
        "mediafiles.MediaFile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )