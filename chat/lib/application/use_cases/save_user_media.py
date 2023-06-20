from quickchat.core.application.use_cases import UseCaseOneEntity
from quickchat.core.domain import UserMediaRepositoryAbstract
from quickchat.core.domain.entities import MediaEntity


class SaveUserMediaUseCase(UseCaseOneEntity):

    def __init__(self, repository: UserMediaRepositoryAbstract):
        self.repository = repository

    def __call__(self, media: MediaEntity):

        self.repository.save_bytes(media.byte_data)