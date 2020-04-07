from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = 'bot'

urlpatterns = [
    path('', csrf_exempt(views.Bot.as_view()), name='bot'),
]