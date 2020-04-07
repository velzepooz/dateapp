from django import forms

from cards.models import Cards


class AddCard(forms.ModelForm):
    class Meta:
        model = Cards
        fields = ("friend_name", "birthdate", "info", "sex")
        labels = {
            "friend_name": 'Имя друга',
            "birthdate": 'Дата рождения',
            "info": 'Информация',
        }
