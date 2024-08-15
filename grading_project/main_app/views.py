from django.shortcuts import render
from . import forms, models, info_table
from django.contrib.auth.models import User


def home_page(request):
    users = User.objects.all()
    gradings = models.Grading.objects.all()

    info_list = []
    for user in users:
        info = info_table.InfoTable(user)
        info.find_user_grading(gradings)
        info_list.append(info)

    context = {
        'info_list': info_list
    }

    return render(request, 'main/home.html', context)


def sign_up_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
