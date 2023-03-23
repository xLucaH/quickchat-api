import uuid

from django.core.signing import Signer

from chat.lib import utils
from chat.lib.domain.room_models import RoomAuthTokenModel

def create_user_token(ip4: str, username: str, user_id: uuid.UUID, room_id: uuid.UUID) -> RoomAuthTokenModel:
    signer = Signer()
    created = utils.now()

    token_dict = {
        'user_id': user_id.hex,
        'username': username,
        'ip4': ip4,
        'created': created.strftime("%Y%m%d%H%%M%S")
    }

    signed_token = signer.sign_object(token_dict)

    return RoomAuthTokenModel(
        id=uuid.uuid4(),
        value=signed_token,
        created=created,
        expiring=utils.add_to_date(created, 'hours', 24),
        last_modified=created,
        user_id=user_id,
        room_id=room_id
    )
