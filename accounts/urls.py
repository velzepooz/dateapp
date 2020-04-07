from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', views.menu, name='menu'),

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),


    path("pwd-reset/",
         auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path(
        "pwd-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        "pwd-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    path(
        "pwd-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),
    path(
        "delete-profile/",
        views.DeleteProfile.as_view(), name="delete-profile"),
]
