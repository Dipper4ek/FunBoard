# game/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import GameRoom, Player

def home(request):
    return render(request, 'Game/home.html')

def create_room(request):
    room = GameRoom.objects.create()
    if request.method == 'POST':
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
    return render(request, 'Game/room.html', {'room': room, 'players': players})
