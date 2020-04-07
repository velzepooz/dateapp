from django.db import models
from django.contrib.auth.models import User


class Cards(models.Model):
    SEX_MALE = 1
    SEX_FEMALE = 2

    SEX_CHOICES = [
        (SEX_MALE, 'Мужчина'),
        (SEX_FEMALE, 'Женщина')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    birthdate = models.DateField(blank=False, null=False)
    friend_name = models.CharField('friend_name', max_length=255, blank=False, null=False)
    info = models.CharField('information', max_length=255, blank=True, null=True)
    sex = models.IntegerField(
        "Пол", choices=SEX_CHOICES, default=SEX_MALE
    )

    def __str__(self):
        return "Карточка друга %s" % self.user.username
