from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = 'cards'

urlpatterns = [
    path('cards', views.Card.as_view(), name='cards'),
    path('add/', views.AddNewCard.as_view(), name='add'),
    path('edit-card/<int:id>', views.CardEdit.as_view(), name='edit-card'),
    path('delete-card/<int:id>', views.CardDelete.as_view(), name='delete-card'),
    path('how-to/', views.how_to, name='how-to'),
]
