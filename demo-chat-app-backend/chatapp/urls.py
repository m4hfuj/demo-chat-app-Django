from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.rooms),
    path('<str:slug>/', views.room)
]
