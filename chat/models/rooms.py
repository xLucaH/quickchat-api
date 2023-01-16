from django.db import models


class Rooms(models.Model):
    room_id = models.CharField(primary_key=True, max_length=60)
    name = models.CharField(max_length=255, blank=True, default=None)
    access_code = models.CharField(max_length=8, blank=False)
    created = models.DateField()
    expiring = models.DateField()
