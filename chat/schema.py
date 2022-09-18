import graphene
from graphene_django import DjangoObjectType
from .models import Rooms, Messages, JoinedRooms


class RoomsType(DjangoObjectType):
    class Meta:
        model = Rooms
        fields = (
            'room_id',
            'access_code',
            'created',
            'expiring',
        )


class MessagesType(DjangoObjectType):
    class Meta:
        model = Messages
        fields = (
            'users_user',
            'rooms_room',
            'created',
            'content',
            'content_type',
        )


class JoinedRoomsType(DjangoObjectType):
    class Meta:
        model = JoinedRooms
        fields = (
            'rooms_room',
            'users_user',
            'last_joined',
        )


class Query(graphene.ObjectType):
    rooms = graphene.List(RoomsType)
    messages = graphene.List(MessagesType)
    joined_rooms = graphene.List(JoinedRoomsType)

    @staticmethod
    def resolve_rooms(self, info, **kwargs):
        # Querying a list
        return Rooms.objects.all()

    @staticmethod
    def resolve_messages(self, info, **kwargs):
        # Querying a list
        return Messages.objects.all()

    @staticmethod
    def resolve_joined_rooms(self, info, **kwargs):
        # Querying a list
        return JoinedRooms.objects.all()

schema = graphene.Schema(query=Query)
