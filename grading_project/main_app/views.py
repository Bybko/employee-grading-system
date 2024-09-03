from django.shortcuts import render, redirect
from . import forms, models, info_table
from django.contrib.auth.models import User


def home_page(request):
    if request.user.is_authenticated:
        user_object = request.user

        if models.Inspectors.objects.filter(user=user_object).exists():
            info = info_table.InfoTable(user_object)
            info.user_role = 'Inspector'
            info.set_faculty(models.Inspectors.objects.get(user=user_object).audited_faculty)

            profiles = models.Profile.objects.all()
            info.find_controlled_users(profiles)
        else:
            user_profile = models.Profile.objects.get(user=user_object)
            info = info_table.InfoTable(user_object)
            info.user_role = 'Teacher'
            info.cathedras = user_profile.teaching_cathedras

            gradings = models.Grading.objects.all()
            criterias = models.Criteria.objects.all()
            info.find_user_grading(gradings, criterias)

        context = {
            'info': info,
            'status_choices': models.Grading.STATUS_CHOICES
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
            if key.startswith('status') and value != '':
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=test_user, used_standard=test_work_title)
                grading.status = value
                grading.save()

    return redirect('home')
