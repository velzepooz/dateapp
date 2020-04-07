from django.contrib.auth import get_user_model
from dateapp.celery import app
import datetime
from django.template import Template, Context

from cards.models import Cards
from accounts.models import Profile
from bot.views import Bot


REPORT_TEMPLATE = """
Все дни рождения всех твоих друзей:

{% for friend in friends %}
{{ friend.friend_name }} - {{ friend.birthdate }}
{% endfor %}
"""

MONTH_TEMPLATE = """
В этом месяце день рождения у:

{% for friend in friends %}
{{ friend.friend_name }} - {{ friend.birthdate }}
{% endfor %}
"""

WEEK_TEMPLATE = """
На этой неделе день рождения у:

{% for friend in friends %}
{{ friend.friend_name }} - {{ friend.birthdate }}
{% endfor %}
"""

DAY_TEMPLATE = """
Сегодня день рождения у:

{% for friend in friends %}
{{ friend.friend_name }} - {{ friend.birthdate }}
{% endfor %}
"""


@app.task
def send_month_report_tg():
    """ Send list of users's friends birthdays this month """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__month=datetime.date.today().month)
        if not friends:
            continue

        t_chat = Profile.objects.get(user_id=user).telegram
        template = Template(MONTH_TEMPLATE)
        Bot.send_message(t_chat, template.render(context=Context({'friends': friends})))


@app.task
def send_week_report_tg():
    """ Send list of users's friends birthdays this week """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__day__gte=datetime.date.today().day,
            birthdate__day__lte=datetime.date.today().day + 6
        )
        if not friends:
            continue

        t_chat = Profile.objects.get(user_id=user).telegram
        template = Template(WEEK_TEMPLATE)
        Bot.send_message(t_chat, template.render(context=Context({'friends': friends})))


@app.task
def send_day_report_tg():
    """ Send list of users's friends birthdays today """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__day=datetime.date.today().day)
        if not friends:
            continue

        t_chat = Profile.objects.get(user_id=user).telegram
        if not t_chat:
            continue

        template = Template(DAY_TEMPLATE)
        Bot.send_message(t_chat, template.render(context=Context({'friends': friends})))
