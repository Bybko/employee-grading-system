from django.shortcuts import render
from . import forms


def home_page(request):
    return render(request, 'main/home.html')


def sign_up_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
