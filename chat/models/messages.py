import uuid
from django.db import models
from quickchat.core.database import model_fields


class Messages(models.Model):

    message_id = model_fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('chat.RoomUsers', models.DO_NOTHING, db_column='rooms_users__user_id', null=False)
    room = models.ForeignKey('chat.Rooms', models.DO_NOTHING, db_column='rooms__room_id', null=False)

    created = models.DateTimeField(null=False)
    content = models.TextField(null=False)
