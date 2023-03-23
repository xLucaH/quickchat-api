# chat/routing.py
from django.urls import path

from chat import views

websocket_urlpatterns = [
    path("rooms/<str:access_code>/", views.RoomsConsumer.as_asgi()),
]