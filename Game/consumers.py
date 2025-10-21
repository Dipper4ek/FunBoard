import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GameRoom, Player, Message

from asgiref.sync import sync_to_async, database_sync_to_async

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        # приєднання до групи
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # надіслати історію чату при підключенні
        room = await database_sync_to_async(GameRoom.objects.get)(code=self.room_code)

        # формуємо список повідомлень у вигляді [{"player": name, "text": text}, ...]
        messages = await database_sync_to_async(
            lambda: [{"player": m.player.name, "text": m.text} for m in room.messages.all()]
        )()

        await self.send(text_data=json.dumps({
            "action": "chat_history",
            "messages": messages
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["action"] == "send_message":
            player_name = data["player"]
            text = data["text"]

            room = await database_sync_to_async(GameRoom.objects.get)(code=self.room_code)
            player = await database_sync_to_async(Player.objects.get)(room=room, name=player_name)
            await database_sync_to_async(Message.objects.create)(room=room, player=player, text=text)

            # відправляємо повідомлення всім учасникам кімнати
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "player": player_name,
                    "text": text
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "action": "new_message",
            "player": event["player"],
            "text": event["text"]
        }))
