from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.data_layer import RoomRepository

from chat.lib.domain.actions.create_room import CreateRoomAction
from chat.lib.domain.actions.get_room import GetRoomAction
from chat.lib.domain.actions.join_room import JoinRoomAction
from chat.lib.domain.actions.authenticate import AuthenticateAction


class RoomActions:

    def __init__(self, repository: RoomRepositoryContract):
        self._repository = repository

        self.create_room = CreateRoomAction(self._repository)
        self.join_room = JoinRoomAction(self._repository)
        self.get_room = GetRoomAction(self._repository)
        self.authenticate = AuthenticateAction(self._repository)


room_actions = RoomActions(
    repository=RoomRepository()
)
