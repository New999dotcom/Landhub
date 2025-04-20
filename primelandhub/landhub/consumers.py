# your_app_name/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, reg_form, Buyer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.seller_id = self.scope['url_route']['kwargs']['seller_id']
        self.buyer_id = self.scope['url_route']['kwargs']['buyer_id']
        self.room_group_name = f'chat_{self.seller_id}_{self.buyer_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'delete':
            message_id = text_data_json.get('messageId')
            if message_id:
                success = await self.delete_message(message_id)
                if success:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {'type': 'chat_delete', 'messageId': message_id}
                    )
        elif action == 'mark_read':
            message_id = text_data_json.get('messageId')
            if message_id:
                await self.mark_message_read(message_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {'type': 'chat_read', 'messageId': message_id}
                )
        elif action == 'mark_all_read':
            await self.mark_all_messages_read()
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_read_all'}
            )
        else:
            message = text_data_json['message']
            sender = text_data_json['sender']
            message_obj = await self.save_message(sender, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    'messageId': str(message_obj.id),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'messageId': event['messageId'],
        }))

    async def chat_delete(self, event):
        await self.send(text_data=json.dumps({
            'action': 'delete',
            'messageId': event['messageId'],
        }))

    async def chat_read(self, event):
        await self.send(text_data=json.dumps({
            'action': 'read',
            'messageId': event['messageId'],
        }))

    async def chat_read_all(self, event):
        await self.send(text_data=json.dumps({
            'action': 'read_all'
        }))

    @database_sync_to_async
    def save_message(self, sender, message):
        seller = reg_form.objects.get(id=self.seller_id)
        buyer = Buyer.objects.get(id=self.buyer_id)
        return Chat.objects.create(
            seller=seller,
            buyer=buyer,
            message=message,
            is_read=False
        )

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            message = Chat.objects.get(
                id=message_id,
                seller__id=self.seller_id,
                buyer__id=self.buyer_id
            )
            message.delete()
            return True
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def mark_message_read(self, message_id):
        try:
            message = Chat.objects.get(
                id=message_id,
                seller__id=self.seller_id,
                buyer__id=self.buyer_id
            )
            message.is_read = True
            message.save()
        except Chat.DoesNotExist:
            pass

    @database_sync_to_async
    def mark_all_messages_read(self):
        Chat.objects.filter(
            seller__id=self.seller_id,
            buyer__id=self.buyer_id,
            is_read=False
        ).update(is_read=True)