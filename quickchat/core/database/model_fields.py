import uuid
from django.db import models


class UUIDField(models.CharField):
    """
    Custom django UUIDField to easily support a uuid with hyphens because by default, this is the length
    of pythons uuid.uuid4() method.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.default = self.generate_uuid
        self.max_length = 32

    @staticmethod
    def generate_uuid():
        return uuid.uuid4().hex
