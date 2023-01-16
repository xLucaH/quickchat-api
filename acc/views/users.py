import json
from uuid import uuid4

from django.contrib.auth import login as user_login, authenticate
from acc.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from quickchat.core import utils


@csrf_exempt
def signup(request):
    if not request.method == 'POST':
        return

    data = json.loads(request.body)

    username = data.get('username')
    raw_password = data.get('password')
    user = User.objects.create_user(
        user_id=uuid4(),
        username=username,
        password=raw_password,
        is_active=True,
        ip=utils.get_client_ip(request),
    )

    user_login(request, user)
    return JsonResponse({"message": "Register successful"}, status=201)


@csrf_exempt
def login(request):
    if not request.method == 'POST' or request.user.is_authenticated:
        return JsonResponse({"message": "Authentication successful"}, status=200)

    data = json.loads(request.body)

    username = data.get('username')
    raw_password = data.get('password')

    user = authenticate(request, username=username, password=raw_password)
    if user is not None:
        user_login(request, user)

    return JsonResponse({"message": "Authentication successful"}, status=200)
