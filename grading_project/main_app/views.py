from django.shortcuts import render


def home_page(request):
    return render(request, 'main/home.html')


#def sign_up_page(request):
#    if request.method == 'POST' :
#        form = RegisterForm(request.POST)
#    else:
#        form = RegisterForm()
#
#    return render(request, )
