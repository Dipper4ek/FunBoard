
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

class AuthGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        # Якщо користувач не авторизований — відхиляємо підключення
        if not user.is_authenticated:
            await self.close()
            raise DenyConnection("Authentication required")

        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        # Приєднуємо користувача до кімнати
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Повідомляємо інших, що підключився користувач
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_joined',
                'username': user.username
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def player_joined(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined',
            'username': event['username']
        }))
