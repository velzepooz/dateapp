import os
import json
import re
import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views import View

from accounts.models import Profile


# URL information
TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN =  os.environ['BOT_TOKEN']

# Message templates
message_start_email = """
Привет! Отправь свой Email с сайта, чтобы я мог понять с кем общаюсь!
"""
message_help = """
Я буду отправлять тебе уведомления о приближающихся праздниках, важных события в жизни твоих близких людей, их днях рождениях и т.д.
"""

# Regex templates
reg_exp_email = "^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$"


class Bot(View):

    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        t_message = t_data["message"]
        t_chat = t_message["chat"]

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        """ Start bot """
        if text == '/start':
            self.send_message(t_chat["id"], message_start_email)

        """ Command /help """
        if text == '/help':
            self.send_message(t_chat["id"], message_help)

        """ Check email """
        if text != '/help' and text != '/start':
            mail = re.search(reg_exp_email, text)
            if mail is not None:
                users = get_user_model()
                if users.objects.filter(email=mail.group(0)).exists():
                    user_id = users.objects.get(email=mail.group(0)).id
                    profile = Profile.objects.get(user_id=user_id)
                    profile.telegram = t_chat["id"]
                    profile.save()
                    self.send_message(t_chat["id"], 'Супер! Бот активирован!')
                else:
                    self.send_message(t_chat["id"], 'Упс! Такой Email не зарегистрирован. Попробуй еще раз')
            else:
                self.send_message(t_chat["id"], 'Пожалуйста, введи Email в формате example@gmail.com')
        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(chat_id, message):
        """ Send message to bot method """
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data
        )
