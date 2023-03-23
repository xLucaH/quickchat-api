from django.db import models
from quickchat.core.database import model_fields


class Rooms(models.Model):

    room_id = model_fields.UUIDField(primary_key=True)

    name = models.CharField(max_length=255, null=False)
    access_code = models.CharField(max_length=8, null=False)
    created = models.DateTimeField(null=False)
    expiring = models.DateTimeField(null=False)
