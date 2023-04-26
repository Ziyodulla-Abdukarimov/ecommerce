import uuid
from django.db import models


# Create your models here.
class MyBaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
