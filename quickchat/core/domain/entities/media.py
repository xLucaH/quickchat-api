from enum import Enum
from quickchat.core.domain import BaseEntity

class MediaType(Enum):

    IMAGE = 0
    VIDEO = 1
    AUDIO = 2



class MediaEntity(BaseEntity):

    user_id: str
    name: str
    byte_data: bytes
    type: MediaType