import uuid
from django.db import models
from quickchat.core.database import model_fields


class MessageAttachments(models.Model):
    attachment_id = model_fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey('chat.Messages', models.CASCADE, db_column='chat_messages__message_id', null=False)

    path = models.TextField(null=False)
    mime_type = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'chat_message_attachments'