# game/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import GameRoom, Player, Message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from .models import GameRoom, generate_room_code
import uuid

import threading
from django.utils import timezone
from .models import GameRoom

def delete_room_after_5min(room_id):
    from .models import GameRoom
    try:
        room = GameRoom.objects.get(id=room_id)
        if not room.is_active:
            room.delete()
    except GameRoom.DoesNotExist:
        pass


def home(request):
    return render(request, 'Game/home.html')

def create_room(request):
    # Генеруємо унікальний код кімнати
    while True:
        code = generate_room_code()
        if not GameRoom.objects.filter(code=code).exists():
            break

    room = GameRoom.objects.create(code=code)
    # Запускаємо таймер на 5 хв (300 секунд)
    threading.Timer(300, delete_room_after_5min, args=[room.id]).start()

    if request.method == 'POST':
        name = request.user.username if request.user.is_authenticated else request.POST.get('name', 'Гравець')
        Player.objects.create(room=room, name=name)
        return redirect('room', room_code=room.code)

    return render(request, 'Game/create_room.html')
def join_room(request):
    if request.method == 'POST':
        code = request.POST.get('code').upper()
        name = request.POST.get('name')
        room = get_object_or_404(GameRoom, code=code)
        if room.players.count() < room.max_players:
            Player.objects.create(room=room, name=name)
            return redirect('room', room_code=room.code)
        else:
            return render(request, 'Game/join.html', {'error': 'Кімната заповнена!'})
    return render(request, 'Game/join.html')


def room_view(request, room_code):
    room = get_object_or_404(GameRoom, code=room_code)
    players = room.players.all()
    messages = room.messages.all().order_by('timestamp')

    # Отримуємо UUID з сесії
    player_uuid = request.session.get("player_uuid")
    player = None

    if player_uuid:
        player = room.players.filter(uuid=player_uuid).first()

    # Якщо авторизований користувач, спробуємо знайти його гравця
    if not player and request.user.is_authenticated:
        player = Player.objects.filter(name=request.user.username, room=room).first()
        if player:
            player_uuid = str(player.uuid)
            request.session["player_uuid"] = player_uuid

    # Якщо гравця немає — створюємо нового
    if not player:
        while True:
            # генеруємо новий UUID
            player_uuid = str(uuid.uuid4())
            if not Player.objects.filter(uuid=player_uuid).exists():
                break

        player = Player.objects.create(
            name=f"Guest {players.count() + 1}",
            room=room,
            uuid=player_uuid
        )
        request.session["player_uuid"] = player_uuid

    # --- Далі твій код (AJAX, чат, start_game) ---
    # ...
    return render(request, 'Game/room.html', {
        'room': room,
        'players': players,
        'player_uuid': player.uuid
    })



def game_board(request, room_code, player_uuid):
    room = get_object_or_404(GameRoom, code=room_code)
    players = room.players.all()
    player = get_object_or_404(Player, room=room, uuid=player_uuid)

    uuid_str = str(player_uuid)  # обовʼязково — JSONField приймає тільки строки

    # AJAX оновлення положення фішок
    if request.GET.get('ajax') == 'state':
        return JsonResponse({
            'board_state': room.board_state,
            'dice_state': room.dice_state
        })

    # AJAX оновлення після кидка кубика
    if request.method == 'POST' and request.content_type == 'application/json':

        try:
            data = json.loads(request.body)

            # Припускаємо, що player_uuid з URL відповідає player_uuid в об'єкті 'player'
            # Припускаємо, що у моделі Player є поля position та dice_value (як рекомендовано)

            # Оновлення значення кубика та/або позиції (якщо дані прийшли з фронтенду)
            if 'dice' in data:
                player.dice_value = data['dice']

            if 'position' in data:  # Якщо ми оновлюємо позицію, а не лише кидок
                player.position = data['position']

            player.save()
            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некоректний JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f"Відсутній ключ у JSON: {e}"}, status=400)

        # ... (інша частина функції view, рендеринг) ...
    return render(request, 'Game/game_board.html', {
        'room': room,
        'players': players,
        'player': player
    })
