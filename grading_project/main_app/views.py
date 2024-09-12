from django.shortcuts import render, redirect
from . import forms, models, info_table
from django.contrib.auth.models import User


def home_page(request):
    if request.user.is_authenticated:
        user_object = request.user

        sort_by = request.GET.get('sort_by', 'used_standard__title')  # 'used_standard__title' will be default sort
        order = request.GET.get('order', 'asc')

        sort_field = {
            'name': 'used_standard__title',
            'normative': 'used_standard__standard_in_points',
            'work_done': 'work_done',
            'points': 'rating',
            'responsible': 'user__user__username',
            'faculty': 'user__teaching_cathedras__owning_faculty__faculty',
            'status': 'status'
        }.get(sort_by, 'used_standard__title') # If the field is not found, the default sorting is by job title

        if order == 'desc':
            sort_field = '-' + sort_field

        if models.Inspectors.objects.filter(user=user_object).exists():
            info = info_table.InfoTable(user_object)
            info.user_role = 'Inspector'
            info.set_faculties(user_object)

            profiles = models.Profile.objects.all()
            info.find_controlled_users(profiles)

            info.sort_all_teachers_gradings(sort_field)
        else:
            user_profile = models.Profile.objects.get(user=user_object)
            info = info_table.InfoTable(user_object)
            info.user_role = 'Teacher'
            info.cathedras = user_profile.teaching_cathedras

            gradings = models.Grading.objects.all()
            info.find_user_grading(gradings)


        context = {
            'info': info,
            'status_choices': models.Grading.STATUS_CHOICES,
            'current_order': 'asc' if order == 'desc' else 'desc'  # Change the order for the next click
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
                print(key.split('-!SePaRaToR!-')[1])
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                profile = models.Profile.objects.get(user=test_user)
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=profile, used_standard=test_work_title)
                grading.work_done = value
                grading.save()
            if key.startswith('points') and value != '':
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                profile = models.Profile.objects.get(user=test_user)
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=profile, used_standard=test_work_title)
                grading.rating = value
                grading.save()
            if key.startswith('status') and value != '':
                test_user = User.objects.get(username=key.split('-!SePaRaToR!-')[1])
                profile = models.Profile.objects.get(user=test_user)
                test_work_title = models.Criteria.objects.get(title=key.split('-!SePaRaToR!-')[2])
                grading = models.Grading.objects.get(user=profile, used_standard=test_work_title)
                grading.status = value
                grading.save()

    return redirect('home')
