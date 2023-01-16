from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from chat.lib import utils

from .models import Rooms, Messages, JoinedRooms


class RoomsType(DjangoObjectType):
    class Meta:
        model = Rooms
        fields = (
            'room_id',
            'access_code',
            'name',
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
            'room',
            'user',
            'last_joined',
        )


class JoinRoom(graphene.Mutation):
    class Arguments:
        access_code = graphene.String()

    join_room = graphene.Field(JoinedRoomsType)

    @classmethod
    def mutate(cls, _, info, access_code):

        room = utils.get_room_by_access_code(access_code)

        if room is None:
            return

        join_room = JoinedRooms(room=room,
                                user=info.context.user,
                                last_joined=utils.now())
        join_room.save()

        return JoinRoom(joined_room=join_room)


class CreateRoom(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    room = graphene.Field(RoomsType)

    @classmethod
    def mutate(cls, _, info, **data):
        now = utils.now()
        room = Rooms()
        room.room_id = utils.generate_room_id()
        room.access_code = utils.generate_room_code()
        room.name = data['name']
        room.created = now
        room.expiring = utils.add_to_date(now, 'hours', 24)
        room.save()

        return CreateRoom(room=room)


class UpdateRooms(graphene.Mutation):
    class Arguments:

        access_code = graphene.String(required=True)

    room = graphene.Field(RoomsType)

    @classmethod
    def mutate(cls, root, info, access_code, room_id):
        room = Rooms.objects.get(pk=room_id)
        room.access_code = access_code
        room.save()

        return UpdateRooms(room=room)


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


class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    update_room = UpdateRooms.Field()
    join_room = JoinRoom.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
