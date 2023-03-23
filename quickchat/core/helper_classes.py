from abc import ABC
from collections.abc import Mapping


class MappingDataclass(Mapping, ABC):
    """
    Custom class that can be used for dataclasses to make allow certain dict functionality like "**" spread or
    conversion of dataclass fields to dict.
    """

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        return iter(self.dict())

    def __len__(self):
        pass

    def dict(self):
        keys = [x for x in self.__dataclass_fields__.keys()]
        return {k: getattr(self, k) for k in keys}