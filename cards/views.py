from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from cards.forms import AddCard
from cards.models import Cards


class Card(LoginRequiredMixin, ListView):
    """ Load cards list"""
    model = Cards
    context_object_name = "cards"
    template_name = "cards.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=u)


class AddNewCard(LoginRequiredMixin, View):
    """ Add new card """
    def post(self, request, *args, **kwargs):
        form = AddCard(request.POST)
        if form.is_valid():
            new_friend = form.save(commit=False)
            new_friend.user = request.user
            new_friend.save()
            return redirect(reverse("cards:cards"))

        return render(request, "cards/add.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = AddCard()
        return render(request, "cards/add.html", {"form": form})


class CardEdit(LoginRequiredMixin, View):
    """ Edit cards """
    def post(self, request, id, *args, **kwargs):
        card = Cards.objects.get(id=id)
        form = AddCard(request.POST, instance=card)
        if form.is_valid():
            card_edit = form.save(commit=False)
            card_edit.owner = request.user
            card_edit.save()
            return redirect(reverse("cards:cards"))

        return render(request, "cards/edit-card.html", {"form": form})

    def get(self, request, id, *args, **kwargs):
        card = Cards.objects.get(id=id)
        form = AddCard(instance=card)
        return render(
            request, "cards/edit-card.html", {"form": form, "card": card})


class CardDelete(LoginRequiredMixin, View):
    """ Delete cards """
    def get(self, request, id):
        card = Cards.objects.get(id=id)
        card.delete()
        return redirect(reverse("cards:cards"))


def how_to(request):
    return render(request, 'cards/how-to.html')
