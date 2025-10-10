import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ProductComment
from products.models import Product
from .serializers import ProductCommentSerializer

User = get_user_model()


class CommentConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time product comments"""

    async def connect(self):
        self.product_slug = self.scope['url_route']['kwargs']['product_slug']
        self.room_group_name = f'product_comments_{self.product_slug}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'new_comment':
            await self.create_comment(data)
        elif action == 'edit_comment':
            await self.edit_comment(data)
        elif action == 'delete_comment':
            await self.delete_comment(data)

    async def create_comment(self, data):
        content = data.get('content')
        parent_id = data.get('parent_comment')
        user = self.scope.get('user')

        if not user or not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'You must be authenticated to comment.'
            }))
            return

        comment = await self.save_comment(user, content, parent_id)

        if comment:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_message',
                    'action': 'new',
                    'comment': comment
                }
            )

    async def edit_comment(self, data):
        comment_id = data.get('comment_id')
        content = data.get('content')
        user = self.scope.get('user')

        if not user or not user.is_authenticated:
            return

        comment = await self.update_comment(comment_id, user.id, content)

        if comment:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_message',
                    'action': 'edit',
                    'comment': comment
                }
            )

    async def delete_comment(self, data):
        comment_id = data.get('comment_id')
        user = self.scope.get('user')

        if not user or not user.is_authenticated:
            return

        success = await self.remove_comment(comment_id, user.id)

        if success:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_message',
                    'action': 'delete',
                    'comment_id': comment_id
                }
            )

    # Receive message from room group
    async def comment_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'comment': event.get('comment'),
            'comment_id': event.get('comment_id')
        }))

    @database_sync_to_async
    def save_comment(self, user, content, parent_id):
        try:
            product = Product.objects.get(slug=self.product_slug)
            parent_comment = None
            if parent_id:
                parent_comment = ProductComment.objects.get(id=parent_id)

            comment = ProductComment.objects.create(
                user=user,
                product=product,
                content=content,
                parent_comment=parent_comment
            )

            serializer = ProductCommentSerializer(comment)
            return serializer.data
        except Exception as e:
            print(f"Error saving comment: {e}")
            return None

    @database_sync_to_async
    def update_comment(self, comment_id, user_id, content):
        try:
            comment = ProductComment.objects.get(id=comment_id, user_id=user_id)
            comment.content = content
            comment.is_edited = True
            comment.save()

            serializer = ProductCommentSerializer(comment)
            return serializer.data
        except ProductComment.DoesNotExist:
            return None

    @database_sync_to_async
    def remove_comment(self, comment_id, user_id):
        try:
            comment = ProductComment.objects.get(id=comment_id)
            # Only allow superuser to delete any comment
            if User.objects.get(id=user_id).is_superuser:
                comment.delete()
                return True
            return False
        except ProductComment.DoesNotExist:
            return False
