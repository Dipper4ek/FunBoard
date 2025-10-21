# game/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import GameRoom, Player

def home(request):
    return render(request, 'Game/home.html')

def create_room(request):
    name = request.POST.get("name", "Хост")
    room = GameRoom.objects.create()
    Player.objects.create(room=room, name=name)
    return redirect('room', room_code=room.code)


def join_room(request):
    if request.method == 'POST':
        code = request.POST.get('code').upper()
        name = request.POST.get('name')
        room = get_object_or_404(GameRoom, code=code)
        if room.players.count() < room.max_players:
            Player.objects.create(room=room, name=name)
            return redirect('room', room_code=room.code)
        else:
            return render(request, 'game/join.html', {'error': 'Кімната заповнена!'})
    return render(request, 'Game/join.html')

def room_view(request, room_code):
    room = get_object_or_404(GameRoom, code=room_code)
    players = room.players.all()

    # Визначаємо поточного гравця
    if request.GET.get("name"):
        player_name = request.GET.get("name")
    elif players.exists():
        player_name = players.first().name  # хост або перший гравець
    else:
        player_name = "Гість"

    return render(request, 'Game/room.html', {
        'room': room,
        'players': players,
        'player_name': player_name
    })
