from django.contrib import admin

from .models import Messages, Rooms, RoomTokens, RoomUsers

# Register your models here.
admin.site.register(Messages)
admin.site.register(Rooms)
admin.site.register(RoomTokens)
admin.site.register(RoomUsers)
