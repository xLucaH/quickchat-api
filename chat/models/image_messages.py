import uuid
from django.db import models


class ImageMessages(models.Model):
    message_id = models.ForeignKey('chat.Messages', models.CASCADE, db_column='chat_messages__message_id', null=False)

    path = models.TextField(null=False)

    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

    class Meta:
        db_table = 'chat_image_messages'