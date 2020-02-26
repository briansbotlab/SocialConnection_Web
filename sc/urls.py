"""SocialConnection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('message/', views.message, name='message'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('admin/', admin.site.urls),

    path('main/Chats/', views.chats, name='chats'),
    path('main/ChatRooms/', views.chatrooms, name='chatrooms'),
    path('main/Users/', views.users, name='users'),
    path('main/Profile/', views.profile, name='profile'),

    path('main/Profile/edit/', views.edit_profile, name='edit_profile'),

    path('main/Users/search/', views.search_users, name='search_users'),
    path('main/ChatRooms/search/', views.search_rooms, name='search_rooms'),


    path('main/Chats/<str:id>/', views.chats_user_room, name='chats_user_room'),


    path('main/Users/<str:userid>/', views.message, name='message'),
    path('main/Users/<str:userid>/interval/', views.message_interval, name='message_interval'),
    path('main/Users/<str:userid>/selectImage/', views.image_message, name='image_message'),
    path('main/Users/<str:userid>/textMsg/', views.text_message, name='text_message'),


    path('main/ChatRooms/<str:roomid>/', views.room_message, name='room_message'),
    path('main/ChatRooms/create/room/', views.create_rooms, name='create_rooms'),
    path('main/ChatRooms/<str:roomid>/interval/', views.room_message_interval, name='room_message_interval'),
    path('main/ChatRooms/<str:roomid>/selectImage/', views.room_image_message, name='room_image_message'),
    path('main/ChatRooms/<str:roomid>/textMsg/', views.room_text_message, name='room_text_message'),
    path('main/ChatRooms/<str:roomid>/setting/', views.room_setting, name='room_setting'),
    path('main/ChatRooms/<str:roomid>/setting/selectImage/', views.room_setting_image, name='room_setting_image'),
    path('main/ChatRooms/<str:roomid>/setting/edit/', views.room_setting_edit, name='room_setting_edit'),
    path('main/ChatRooms/<str:roomid>/setting/<str:userid>/', views.room_setting_chat, name='room_setting_chat'),





]
