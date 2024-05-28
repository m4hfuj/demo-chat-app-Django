# demo-chat-app
A demo chat app using websocket in django

![My Image](./demo-chat-app-backend/chatapp.png)

## Step 1:
A simple authorization from here
https://learndjango.com/tutorials/django-login-and-logout-tutorial

## Step 2:
Create a chatapp and add


### Add in settings.py

    INSTALLED_APPS = [
        'daphne',
        'channels',
        
        ................
        
        'chatapp'
    ]

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

    ASGI_APPLICATION = 'core.asgi.application'


### Add asgi.py

    # core/asgi.py
    import os
    from django.core.asgi import get_asgi_application
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')
    
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter , URLRouter
    from chatapp import routing
    
    application = ProtocolTypeRouter(
        {
            "http" : get_asgi_application() , 
            "websocket" : AuthMiddlewareStack(
                URLRouter(
                    routing.websocket_urlpatterns
                )    
            )
        }
    )


### Add Routing.py

    # chatapp/Routing.py
    from django.urls import path , include, re_path
    from .consumers import ChatConsumer
    
    # Here, "" is routing to the URL ChatConsumer which 
    # will handle the chat functionality.
    websocket_urlpatterns = [
        re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
    ]


### Add Consumers.py

    # chatapp/Consumers.py
    import json
    from channels.generic.websocket import AsyncWebsocketConsumer
    
    class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_slug']
            self.roomGroupName = f'chat_{self.room_name}'
    
            await self.channel_layer.group_add(
                self.roomGroupName ,
                self.channel_name
            )
            await self.accept()
    
        async def disconnect(self , close_code):
            await self.channel_layer.group_discard(
                self.roomGroupName , 
                self.channel_layer 
            )
    
        async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            username = text_data_json["username"]
            await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "message" : message , 
                    "username" : username ,
                })
    
        async def sendMessage(self , event) : 
            message = event["message"]
            username = event["username"]
            await self.send(text_data = json.dumps({"message":message, "username":username}))


### Add room.html

    <-- templates/room.html --/>
    {% extends "base.html" %}
    
    {% block content %}
    {% if user.is_authenticated %}
    
    <p>Hi {{ user.username }}!</p>
    <h2>You are in chat room.</h2>
    
    <div
        class="chat__item__container"
        id="id_chat_item_container"
        style="font-size: 20px"
    >
        <br />
        <input type="text" id="id_message_send_input" />
        <button type="submit" id="id_message_send_button">Send Message</button>
        <br />
        <br />
    </div>
    {{slug|json_script:'room_slug'}}
    <script>
        const roomSlug = JSON.parse(document.getElementById('room_slug').textContent);
        // alert(roomSlug);
    
        const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomSlug + "/");
        console.log("Connected to: " + chatSocket['url'])
    
        chatSocket.onopen = function (e) {
            console.log("The connection was setup successfully !");
        };
        chatSocket.onclose = function (e) {
            console.log("Something unexpected happened !");
        };
        document.querySelector("#id_message_send_input").focus();
        document.querySelector("#id_message_send_input").onkeyup = function (e) {
            if (e.keyCode == 13) {
                document.querySelector("#id_message_send_button").click();
            }
        };
        document.querySelector("#id_message_send_button").onclick = function (e) {
            var messageInput = document.querySelector(
                "#id_message_send_input"
            ).value;
            chatSocket.send(JSON.stringify({ message: messageInput, username : "{{request.user.username}}"}));
        };
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            var div = document.createElement("div");
            div.innerHTML = data.username + ": " + data.message;
            document.querySelector("#id_message_send_input").value = "";
            document.querySelector("#id_chat_item_container").appendChild(div);
        };
    </script>
    
    {% endif %}
    {% endblock %}




