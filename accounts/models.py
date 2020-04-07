from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    telegram = models.CharField('telegram', max_length=64, blank=True, null=True)
    messenger = models.CharField('messenger', max_length=255, blank=True, null=True)
    phone_number = models.CharField('phone_number', max_length=64, blank=True, null=True)

    def __str__(self):
        return "Профиль пользователя %s" % self.user.username

    def create_profile(sender, **kwargs):
        """
        Create db when user is register
        """
        if kwargs['created']:
            Profile.objects.create(user=kwargs['instance'])
    models.signals.post_save.connect(create_profile, sender=User)
