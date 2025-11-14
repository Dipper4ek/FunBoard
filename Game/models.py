# game/models.py
import string, random
from django.db import models
import uuid

def generate_room_code():
    return ''.join(random.choices(string.digits, k=4))


class GameRoom(models.Model):
    code = models.CharField(max_length=8, unique=True)
    max_players = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Для зберігання стану дошки
    board_state = models.JSONField(default=dict)  # {player_uuid: {"x": 0, "y": 0}}
    dice_state = models.JSONField(default=dict)   # {player_uuid: last_dice_roll}

    def __str__(self):
        return self.code
class Player(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # <<< це потрібно!
    joined_at = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(default=0)  # Нове поле: поточна позиція
    dice_value = models.IntegerField(default=1)  # Нове поле: останній кидок кубика

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='messages')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name}: {self.content[:20]}"

