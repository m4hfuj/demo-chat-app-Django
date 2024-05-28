from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=10)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # slug = models.SlugField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
