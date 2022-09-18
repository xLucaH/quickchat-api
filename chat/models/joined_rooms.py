from django.db import models


class JoinedRooms(models.Model):
    rooms_room = models.ForeignKey('chat.Rooms', models.DO_NOTHING, db_column='rooms__room_id')
    users_user = models.ForeignKey('acc.User', models.DO_NOTHING, db_column='users__user_id')
    last_joined = models.DateField()

    class Meta:
        db_table = f'chat_joined_rooms'
