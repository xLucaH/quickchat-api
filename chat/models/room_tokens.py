import uuid
from django.db import models
from quickchat.core.database import model_fields


class RoomTokens(models.Model):

    token_id = model_fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    token = models.CharField(max_length=255, blank=False, null=False, unique=True)
    created = models.DateTimeField(null=False)
    expiring = models.DateTimeField(null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)

    room_user = models.ForeignKey('chat.RoomUsers', models.DO_NOTHING, db_column='room_users__user_id', null=False)
    room = models.ForeignKey('chat.Rooms', models.DO_NOTHING, db_column='room__room_id', null=False)

    class Meta:
        db_table = 'chat_room_tokens'
