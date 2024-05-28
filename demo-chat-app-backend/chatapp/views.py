from django.shortcuts import render
from .models import Room


def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {
        'rooms': rooms,
    })


def room(request, slug):
    # room = Roo
    # slug = slug
    return render(request, 'room.html', {
        'slug': slug
    })
