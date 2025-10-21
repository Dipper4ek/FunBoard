
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        # приєднуємось до групи кімнати
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # повідомляємо інших, що новий гравець підключився
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_joined',
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def player_joined(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_players'
        }))
