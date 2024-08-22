from django.shortcuts import render, redirect
from . import forms, models, info_table
from django.contrib.auth.models import User


def home_page(request):
    user = request.user
    gradings = models.Grading.objects.all()
    criterias = models.Criteria.objects.all()

    info = info_table.InfoTable(user)
    info.find_user_grading(gradings, criterias)

    context = {
        'info': info
    }

    return render(request, 'main/home.html', context)


def sign_up_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def save_form_function(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('work_done_') and value is not '':
                test_user = User.objects.get(username=key.split('_')[2])
                test_work_title = models.Criteria.objects.get(title=key.split('_')[3])
                grading = models.Grading.objects.get(user=test_user, used_standard=test_work_title)
                grading.work_done = value
                grading.save()
            if key.startswith('points_') and value is not '':
                test_user = User.objects.get(username=key.split('_')[1])
                test_work_title = models.Criteria.objects.get(title=key.split('_')[2])
                grading = models.Grading.objects.get(user=test_user, used_standard=test_work_title)
                grading.rating = value
                grading.save()

    return redirect('home')
