import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import MediaFile, MediaLink

User = get_user_model()


class MediaFileApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
        )
        self.other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def _upload(self):
        file = SimpleUploadedFile(
            "photo.jpg",
            b"file-content",
            content_type="image/jpeg",
        )
        return self.client.post(
            reverse("media-list"),
            {"file": file},
            format="multipart",
        )

    def test_upload_creates_media_file(self):
        response = self._upload()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MediaFile.objects.filter(id=response.data["id"]).exists())

    def test_retrieve_returns_metadata(self):
        media = MediaFile.objects.create(
            file=SimpleUploadedFile(
                "photo.jpg",
                b"file-content",
                content_type="image/jpeg",
            ),
            original_name="photo.jpg",
            size=12,
        )
        response = self.client.get(reverse("media-detail", args=[media.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(media.id))
        self.assertEqual(response.data["original_name"], "photo.jpg")

    def test_retrieve_missing_returns_404(self):
        response = self.client.get(reverse("media-detail", args=["00000000-0000-0000-0000-000000000000"]))
        self.assertEqual(response.status_code, 404)

    def test_retrieve_requires_auth(self):
        media = MediaFile.objects.create(
            file=SimpleUploadedFile(
                "photo.jpg",
                b"file-content",
                content_type="image/jpeg",
            ),
            original_name="photo.jpg",
            size=12,
        )
        anonymous = APIClient()
        response = anonymous.get(reverse("media-detail", args=[media.id]))
        self.assertEqual(response.status_code, 401)

    def test_list_by_entity(self):
        media = MediaFile.objects.create(
            file=SimpleUploadedFile(
                "photo.jpg",
                b"file-content",
                content_type="image/jpeg",
            ),
            original_name="photo.jpg",
            size=12,
        )
        MediaLink.objects.create(
            media_file=media,
            entity_type="user",
            entity_id=self.user.id,
        )
        response = self.client.get(
            reverse("media-list"),
            {"entity_type": "user", "entity_id": self.user.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], str(media.id))

    def test_list_paginates_by_default(self):
        for i in range(25):
            MediaFile.objects.create(
                file=SimpleUploadedFile(
                    f"photo_{i}.jpg",
                    b"file-content",
                    content_type="image/jpeg",
                ),
                original_name=f"photo_{i}.jpg",
                size=12,
            )
        response = self.client.get(reverse("media-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 25)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertIsNotNone(response.data["next"])

    def test_list_respects_page_size_and_max(self):
        for i in range(110):
            MediaFile.objects.create(
                file=SimpleUploadedFile(
                    f"photo_{i}.jpg",
                    b"file-content",
                    content_type="image/jpeg",
                ),
                original_name=f"photo_{i}.jpg",
                size=12,
            )
        response = self.client.get(
            reverse("media-list"),
            {"page_size": 5},
        )
        self.assertEqual(response.data["count"], 110)
        self.assertEqual(len(response.data["results"]), 5)

        response = self.client.get(
            reverse("media-list"),
            {"page_size": 999},
        )
        self.assertEqual(response.data["count"], 110)
        self.assertEqual(len(response.data["results"]), 100)

    def test_list_partial_params_returns_400(self):
        response = self.client.get(
            reverse("media-list"),
            {"entity_type": "user"},
        )
        self.assertEqual(response.status_code, 400)
