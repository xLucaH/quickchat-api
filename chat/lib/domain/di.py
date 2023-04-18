from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.actions.create_room import CreateRoomAction
from chat.lib.domain.actions.get_room import GetChatAction
from chat.lib.domain.actions.join_room import JoinRoomAction
from chat.lib.domain.actions.authenticate import AuthenticateAction
from chat.lib.domain.actions.disconnect_user import DisconnectUser
from chat.lib.domain.actions.log_message import LogMessageAction

from chat.lib.data_layer import RoomRepository


class RoomActions:

    def __init__(self, repository: RoomRepositoryContract):
        self._repository = repository

        self.create_room = CreateRoomAction(self._repository)
        self.join_room = JoinRoomAction(self._repository)
        self.get_chat = GetChatAction(self._repository)
        self.authenticate = AuthenticateAction(self._repository)
        self.disconnect_user = DisconnectUser(self._repository)
        self.log_message = LogMessageAction(self._repository)

room_actions = RoomActions(
    repository=RoomRepository()
)
