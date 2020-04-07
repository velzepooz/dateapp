from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from dateapp.celery import app
import datetime

from .models import Cards


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
def send_all_friends_birthdate_email():
    """
    Send list of users's friends birthdays
    """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user)
        if not friends:
            continue

        template = Template(REPORT_TEMPLATE)

        send_mail(
            'Твои друзья',
            template.render(context=Context({'friends': friends})),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )



@app.task
def send_month_report_email():
    """
    Send list of users's friends birthdays this month
    """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__month=datetime.date.today().month)
        if not friends:
            continue

        template = Template(MONTH_TEMPLATE)

        send_mail(
            'Твои друзья',
            template.render(context=Context({'friends': friends})),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )


@app.task
def send_week_report_email():
    """
    Send list of users's friends birthdays this week
    """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__day__gte=datetime.date.today().day,
            birthdate__day__lte=datetime.date.today().day + 6
        )
        if not friends:
            continue

        template = Template(WEEK_TEMPLATE)

        send_mail(
            'Твои друзья',
            template.render(context=Context({'friends': friends})),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )


@app.task
def send_day_report_email():
    """
    Send list of users's friends birthdays today
    """
    for user in get_user_model().objects.all():
        friends = Cards.objects.filter(user=user).filter(
            birthdate__day=datetime.date.today().day)
        if not friends:
            continue

        template = Template(DAY_TEMPLATE)

        send_mail(
            'Твои друзья',
            template.render(context=Context({'friends': friends})),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )





