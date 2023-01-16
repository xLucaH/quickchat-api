# chat/routing.py
from django.urls import path

from chat import views

websocket_urlpatterns = [
    path("rooms/<str:room_name>/", views.RoomsConsumer.as_asgi()),
]