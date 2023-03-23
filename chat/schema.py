import graphene

from chat.lib.domain import room_models
from chat.lib.domain.di import room_actions

from .models import Rooms


class RoomsType(graphene.ObjectType):

    room_id = graphene.String()
    access_code = graphene.String()
    name = graphene.String()
    created = graphene.DateTime()
    expiring = graphene.DateTime()
    url = graphene.String()


class MessagesType(graphene.ObjectType):

    content = graphene.String()


class JoinRoomType(graphene.ObjectType):

    value = graphene.String()
    expiring = graphene.String()


class JoinRoom(graphene.Mutation):

    class Arguments:
        access_code = graphene.String()
        username = graphene.String()

    token = graphene.Field(JoinRoomType)

    @staticmethod
    def resolve_token(token: room_models.RoomAuthTokenModel, info: graphene.ResolveInfo):
        return JoinRoomType(
            value=token.value,
            expiring=str(token.expiring)
        )

    @classmethod
    def mutate(cls, _, info: graphene.ResolveInfo, access_code, username, **data):
        request = info.context

        token = room_actions.join_room(
            request=request,
            username=username,
            access_code=access_code
        )
        return token

class CreateRoom(graphene.Mutation):

    class Arguments:
        name = graphene.String()

    room = graphene.Field(RoomsType)
    url = graphene.String()

    @staticmethod
    def resolve_room(room: room_models.RoomModel, info):
        return RoomsType(
            room_id=room.id,
            name=room.name,
            access_code=room.access_code,
            created=room.created,
            expiring=room.expiring,
            url=room.url
        )

    @classmethod
    def mutate(cls, _, info: graphene.ResolveInfo, **data):
        return room_actions.create_room(room_name=data['name'])


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


class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    update_room = UpdateRooms.Field()
    join_room = JoinRoom.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
