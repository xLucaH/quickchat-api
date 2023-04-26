import os
from typing import Tuple, List
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File


class MediaFolder:
    """
    Provides an interface to handle media files and folders inside our project.
    The class implements some boilerplate for us in order to write short and clean code when working with media files.
    """

    def __init__(self, folder_id: str = None, raise_exception=True) -> None:
        self.folder_id = folder_id
        self.create_date = self.folder_id[:14]

        self._root_dir = settings.BASE_DIR  # Absolute root path of django project.
        self._media_root = settings.MEDIA_ROOT  # Absolute path to base media dir.
        self._media_relative = os.path.relpath(self._media_root, self._root_dir)  # relative path from root project.

        # Media host url to guid folder.
        self.media_url = build_media_url(self.folder_id)

        self.path_full = os.path.join(self._media_root, self.folder_id)
        self.path_relative = os.path.join(self._media_relative, self.folder_id)

        self.folder_rights = 0o776

        self._files = self.read(raise_exception)

    def create(self) -> None:
        """
        Creates a guid folder inside the media directory.
        """
        if not os.path.exists(self.path_full):
            os.mkdir(self.path_full)
            os.chmod(self.path_full, self.folder_rights)

    def save_file(self, file: File, path: str) -> Tuple[str, str]:
        """
        Saves a file inside the media folder.

        :param file: A django file instance
        :param path: Path in media folder to save file to

        :return: Tuple of full write path and relative write path from media folder.
        """

        # Full write path of file
        write_path = os.path.join(self.path_full, path)
        relative_path = os.path.join(self.folder_id, path)

        default_storage.save(write_path, file)

        self._files.append(write_path)

        return write_path, relative_path

    def build_media_url(self, *args: str) -> str:
        """
        Works like os.path.join by concatenating all parameters to the media url of the specific folder.
        :param args: variable amount of strings representing one block of the url path.
        :return:
        """
        joined_paths = '/'.join(args)
        return build_media_url(f'{self.folder_id}/{joined_paths}')

    def get_write_path(self, rel_path) -> Tuple[str, str]:
        return os.path.join(self.path_full, rel_path), os.path.join(self.folder_id, rel_path)

    @staticmethod
    def _is_existing(path, raise_exception=False) -> bool:
        """
        Internal method to check, whether the given path does exist in the media folder.
        :param path: path of media folder/file.
        :param raise_exception: bool to optionally throw an exception if folder does not exist

        :return: True if folder with given guid exists, false if not.
        """
        if os.path.isdir(path):
            return True

        if raise_exception:
            raise NotADirectoryError(f'Folder {path} does not exist.')

        return False

    def read(self, raise_exception=True, filter_list=None) -> List[str]:
        """
        Reads the folder's content.

        :return: List of all files in media folder or filtered results if filter_list is given.
        """
        is_existing = self._is_existing(self.path_full, raise_exception=raise_exception)

        if not is_existing and not raise_exception:
            return []

        self._files = os.listdir(self.path_full)

        if filter_list is None:
            return self._files

        return [x for x in self._files if ext_and_filename(x)[0].lower() in filter_list]

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def root_path(self):
        return self._media_root


def build_media_url(relative_path) -> str:
    """
    Builds an url with a relative path with its origin from the media folder.

    :param relative_path
    :return: absolute media url
    """
    base_path = urljoin(settings.HOST_URL, settings.MEDIA_URL)
    return urljoin(base_path, relative_path)


def ext_and_filename(path: str) -> Tuple[str, str]:
    """
    Return's the filename, e.g "my_file" and it's extension ".ply" as a tuple.

    :param path: The path with a file
    :return: [file extension, filename only]
    """
    return os.path.splitext(path)[1], os.path.splitext(os.path.basename(path))[0]