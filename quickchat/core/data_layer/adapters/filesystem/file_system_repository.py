import os
from quickchat.core.domain import UserMediaRepositoryAbstract


class FileSystemRepository(UserMediaRepositoryAbstract):

    def is_path_existing(self, path: str) -> bool:
        return os.path.exists(path)

    def save_bytes(self, bytes_data: bytes, path: str):

        with open(path, "wb") as f:
            f.write(bytes_data)

