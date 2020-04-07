from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def information(request):
    return render(request, 'information.html')


def policy(request):
    return render(request, 'policy.html')


def profile_deleted(request):
    return render(request, 'profile-deleted.html')
