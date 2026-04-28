from django.db import models
from accounts.models import CustomUser
from listings.models import Listing


class ChatRoom(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='chats')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer_chats')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['listing', 'buyer', 'seller']
        verbose_name = 'Chat xonasi'
        verbose_name_plural = 'Chat xonalari'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.buyer.username} - {self.seller.username} ({self.listing.title})"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
