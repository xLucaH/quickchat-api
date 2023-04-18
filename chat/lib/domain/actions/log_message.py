from chat.lib.domain import RoomRepositoryContract
from chat.lib.domain.room_models import RoomMessageModel


class LogMessageAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(self, message: RoomMessageModel):
        self.repository.save_message(message)