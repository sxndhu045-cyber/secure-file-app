from django.db import models
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=24)

    def __str__(self):
        return self.file.name