from django.contrib import admin

from .models import Messages, Rooms, JoinedRooms

# Register your models here.
admin.site.register(Messages)
admin.site.register(Rooms)
admin.site.register(JoinedRooms)
