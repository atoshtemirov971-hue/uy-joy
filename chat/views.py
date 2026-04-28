from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Message
from listings.models import Listing


@login_required
def chat_list_view(request):
    rooms = ChatRoom.objects.filter(
        buyer=request.user
    ) | ChatRoom.objects.filter(
        seller=request.user
    )
    rooms = rooms.order_by('-updated_at')
    return render(request, 'chat/list.html', {'rooms': rooms})


@login_required
def chat_room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.buyer, room.seller]:
        messages.error(request, 'Ruxsat yo\'q!')
        return redirect('chat-list')
    chat_messages = room.messages.all()
    room.messages.filter(is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': chat_messages,
    })


@login_required
def chat_start_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if listing.owner == request.user:
        messages.error(request, 'O\'z e\'loningizga xabar yubora olmaysiz!')
        return redirect('listing-detail', slug=listing.slug)
    room, created = ChatRoom.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        seller=listing.owner
    )
    return redirect('chat-room', room_id=room.id)
