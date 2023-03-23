import random
import string
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from django.conf import settings

from chat.models import Rooms


def now() -> datetime.date:
    """
    Returns the current time as date.
    :return:
    """
    return datetime.now()


def generate_room_id() -> str:
    """
    Generates a random uuid4 id.
    :return: uuid4 as string.
    """
    return str(uuid4())


def generate_room_code() -> str:
    """
    Generates a random id for a room.

    :return: random 8 char long room ID
    """
    return ''.join((random.choice(string.ascii_uppercase + string.digits) for i in range(8)))


def add_to_date(in_date: datetime.date, time_format: str, value: int) -> datetime.date:
    """
    Add's a specific time value to the input date.

    :param in_date: The date you want to add time to.
    :param time_format: The time format you want to use, e.g 'days', 'hours'.
    :param value: The value for the time_format
    :return: the newly calculated date
    """
    kwargs = {time_format: value}

    return in_date + timedelta(**kwargs)


def is_room_existing(access_code: str) -> bool:
    """
    Check's if the room with the given access exists inside the database.

    :param access_code: The room access code to check for
    :return: True if the room exists else False
    """
    return len(Rooms.objects.filter(access_code=access_code)) == 1


def get_room_by_access_code(access_code: str) -> Union[Rooms, None]:
    try:
        return Rooms.objects.filter(access_code=access_code).get()
    except Rooms.DoesNotExist:
        return None


def build_room_url(access_code: str) -> str:
    return f'{settings.FRONTEND_URL}rooms/{access_code}/'
