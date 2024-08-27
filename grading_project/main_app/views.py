from django.shortcuts import render, redirect
from . import forms, models, info_table
from django.contrib.auth.models import User


def home_page(request):
    if request.user.is_authenticated:
        user_object = request.user
        gradings = models.Grading.objects.all()
        criterias = models.Criteria.objects.all()
        role = models.Profile.objects.get(user=user_object)

        info = info_table.InfoTable(user_object)
        info.set_role(role)

        if info.user_role == 'Работник':
            info.find_user_grading(gradings, criterias)
        elif info.user_role == 'Проверяющий':
            users = User.objects.all()
            info.find_controlled_users(users)

        context = {
            'info': info
        }

        return render(request, 'main/home.html', context)
    else:
        return redirect('login')


def sign_up_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def save_form_function(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('work_done') and value != '':
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=test_user, used_standard=test_work_title)
                grading.work_done = value
                grading.save()
            if key.startswith('points') and value != '':
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=test_user, used_standard=test_work_title)
                grading.rating = value
                grading.save()

    return redirect('home')
