import os
import uuid
from datetime import datetime
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from chat.lib.domain.di import room_actions
from chat.lib.domain.files.media_folder import MediaFolder, ext_and_filename
from chat.lib.domain.room_models import RoomMessageModel, MessageType, RoomMessageAttachmentModel

from chat.lib.channel_layers.channel_methods import ROOM_CHANNEL_METHOD

from chat.lib.events import EventType, ChannelEvent


@csrf_exempt
def upload_file(request: HttpRequest, room_access_code: str, *args, **kwargs):
    if request.method != 'POST':
        return

    event_mime_map = {
        'image': (EventType.IMAGE_MESSAGE, MessageType.IMAGE),
        'video': (EventType.VIDEO_MESSAGE, MessageType.VIDEO),
        'audio': (EventType.AUDIO_MESSAGE, MessageType.AUDIO),
    }

    user = room_actions.authenticate(request.headers['Authorization'])

    text = request.POST.get('text', "")

    file: InMemoryUploadedFile = request.FILES['file']
    filename = uuid.uuid4().hex + ext_and_filename(file.name)[0]
    folder = MediaFolder(room_access_code, raise_exception=False)
    folder.create()

    file_save_path_full, file_save_path_relative = folder.get_write_path(os.path.join('attachments', filename))
    folder.save_file(file, file_save_path_full)

    event_type = event_mime_map[file.content_type.split("/")[0]][0]
    message_type = event_mime_map[file.content_type.split("/")[0]][1]

    message = RoomMessageModel(
        id=uuid.uuid4(),
        created=datetime.now(),
        sender_id=user.id,
        content=text,
        room_id=user.room_id,
        message_type=message_type
    )
    attachment = RoomMessageAttachmentModel(
        id=uuid.uuid4(),
        message_id=message.id,
        path=file_save_path_relative,
        mime_type=file.content_type,
    )
    message.attachments.append(attachment)

    room_actions.log_message(message)

    message_event = ChannelEvent(
        method=ROOM_CHANNEL_METHOD,
        event_type=event_type,
        data=message.to_dict()
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"chat_{room_access_code}", message_event.serialize())

    return JsonResponse(status=200, data={'status': 'success'}, safe=False)


@csrf_exempt
def change_profile_picture(request: HttpRequest, room_access_code: str):
    if request.method != 'POST':
        return

    user = room_actions.authenticate(request.headers['Authorization'])
    chat = room_actions.get_chat(room_access_code)

    file: InMemoryUploadedFile = request.FILES['file']
    filename = uuid.uuid4().hex + ext_and_filename(file.name)[0]
    folder = MediaFolder(room_access_code, raise_exception=False)
    folder.create()

    file_save_path_full, file_save_path_relative = folder.get_write_path(os.path.join('profile_pics', filename))
    folder.save_file(file, file_save_path_full)

    message = RoomMessageModel(
        id=uuid.uuid4(),
        created=datetime.now(),
        sender_id=chat.room.id,
        content=f'{user.username} changed his/her profile picture.',
        room_id=user.room_id,
        message_type=MessageType.SYSTEM
    )

    room_actions.log_message(message)

    message_event = ChannelEvent(
        method=ROOM_CHANNEL_METHOD,
        event_type=EventType.SYSTEM_MESSAGE,
        data=message.to_dict()
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"chat_{room_access_code}", message_event.serialize())

    return JsonResponse(status=200, data={'status': 'success'}, safe=False)
