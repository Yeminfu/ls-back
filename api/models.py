from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.TextField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.title