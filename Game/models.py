# game/models.py
import string, random
from django.db import models

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class GameRoom(models.Model):
    code = models.CharField(max_length=6, default=generate_room_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_players = models.IntegerField(default=5)

    def __str__(self):
        return self.code

class Player(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=50)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='messages')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name}: {self.text[:20]}"