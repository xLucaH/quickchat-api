from abc import ABC, abstractmethod


class UserMediaRepositoryAbstract(ABC):

    @abstractmethod
    def is_path_existing(self, path: str) -> bool:
        pass

    @abstractmethod
    def save_bytes(self, bytes_data: bytes, path: str) -> None:
        pass
