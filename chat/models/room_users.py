import uuid
from django.db import models
from quickchat.core.database import model_fields


class RoomUsers(models.Model):

    user_id = model_fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    room = models.ForeignKey('chat.Rooms', models.DO_NOTHING, null=False, db_column='rooms__room_id')

    username = models.CharField(max_length=40, null=False)
    ip4 = models.CharField(max_length=19, null=True)
    date_joined = models.DateTimeField(null=False)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(null=False)

    is_online = models.BooleanField(null=False)

    class Meta:
        db_table = 'chat_room_users'
