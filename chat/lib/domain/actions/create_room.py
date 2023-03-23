import uuid
import random
import string

from quickchat.core import utils

from chat.lib.domain.contracts import RoomRepositoryContract
from .. import room_models


class CreateRoomAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(self, room_name: str) -> room_models.RoomModel:

        now = utils.now()

        room = self.repository.create_room(
            room_models.RoomModel(
                id=uuid.uuid4(),
                name=room_name,
                access_code=self.generate_room_code(),
                created=now,
                expiring=utils.add_to_date(now, 'hours', 24)
            )
        )

        return room

    @staticmethod
    def generate_room_code() -> str:
        """
        Generates a random id for a room.

        :return: random 8 char long room ID
        """
        return ''.join((random.choice(string.ascii_uppercase + string.digits) for i in range(8)))