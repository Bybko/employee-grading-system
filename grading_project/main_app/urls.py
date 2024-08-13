from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('home', views.home_page, name='home'),
    path('sign-up', views.sign_up_page, name='sign-up'),
]