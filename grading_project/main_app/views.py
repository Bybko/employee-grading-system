from django.shortcuts import render
from . import forms, models, info_table


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
