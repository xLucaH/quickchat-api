from django.db import models


class Messages(models.Model):
    users_user = models.ForeignKey('acc.User', models.DO_NOTHING, db_column='users__user_id')
    rooms_room = models.ForeignKey('chat.Rooms', models.DO_NOTHING, db_column='rooms__room_id')
    created = models.DateField()
    content = models.CharField(max_length=1024)
    content_type = models.CharField(max_length=40)
