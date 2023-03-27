from abc import ABC, abstractmethod
from typing import Union, List
from uuid import UUID

from chat.lib.domain.room_models import RoomModel, RoomUserModel, RoomAuthTokenModel, RoomMessageModel


class RoomRepositoryContract(ABC):

    @abstractmethod
    def get_room_by_access_code(self, access_code: str) -> Union[RoomModel, None]:
        pass

    @abstractmethod
    def get_room_by_id(self, room_id: str) -> Union[RoomModel, None]:
        pass

    @abstractmethod
    def get_room_messages(self, room_id: UUID) -> List[RoomMessageModel]:
        pass

    @abstractmethod
    def get_room_users(self, room_id: UUID) -> List[RoomUserModel]:
        pass

    @abstractmethod
    def create_room(self, room: RoomModel) -> RoomModel:
        pass

    @abstractmethod
    def create_user(self, user: RoomUserModel) -> RoomUserModel:
        pass

    @abstractmethod
    def create_room_token(self, room_token: RoomAuthTokenModel) -> RoomAuthTokenModel:
        pass

    @abstractmethod
    def get_room_token(self, token: str) -> RoomAuthTokenModel:
        pass

    def get_user_by_id(self, user_id: str) -> RoomUserModel:
        pass