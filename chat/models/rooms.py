from django.db import models


class Rooms(models.Model):
    room_id = models.CharField(primary_key=True, max_length=60)
    access_code = models.CharField(max_length=8, blank=False)
    created = models.DateField()
    expiring = models.DateField()
