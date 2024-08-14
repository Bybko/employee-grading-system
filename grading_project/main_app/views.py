from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User


def home_page(request):
    users = User.objects.all()
    context = {
        'users': users
    }

    return render(request, 'main/home.html', context)


def sign_up_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
