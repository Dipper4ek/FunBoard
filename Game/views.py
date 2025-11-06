# game/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import GameRoom, Player, Message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
def home(request):
    return render(request, 'Game/home.html')
def create_room(request):
    room = GameRoom.objects.create()
    if request.method == 'POST':
        name = request.user.username
        name = request.POST.get('name')

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

    # AJAX оновлення
    if request.GET.get('ajax') == 'players':
        return JsonResponse({"players": [{"name": p.name} for p in players]})

    if request.GET.get('ajax') == 'messages':
        return JsonResponse({
            "messages": [
                {"player": m.player.name, "content": m.content, "timestamp": m.timestamp.strftime('%H:%M:%S')}
                for m in messages
            ]
        })

    # Чат
    if request.method == "POST" and request.POST.get('content'):
        player = Player.objects.filter(name=request.user.username, room=room).first()
        if not player:
            player = Player.objects.create(name=request.user.username, room=room)
        Message.objects.create(room=room, player=player, content=request.POST.get('content'))

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'player': player.name, 'content': request.POST.get('content')})

    # Якщо натиснули кнопку “Почати гру” — редірект
    if request.method == "POST" and "start_game" in request.POST:
        return redirect('game_board', room_code=room.code)

    return render(request, 'Game/room.html', {'room': room, 'players': players})


# Сторінка гри
def game_board(request, room_code):
    room = get_object_or_404(GameRoom, code=room_code)
    players = room.players.all()
    return render(request, 'Game/game_board.html', {'room': room, 'players': players})
