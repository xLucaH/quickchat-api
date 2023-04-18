from django.db import models


class MessageTypes(models.Model):

    message_type_id = models.IntegerField(primary_key=True, null=False)
    technical_name = models.CharField(max_length=20, null=False)
    display_name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'chat_message_types'