from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('home', views.home_page, name='home'),
    path('save-form', views.save_form_function, name='save-form'),
    path('approve-all', views.approve_all_function, name='approve-all'),
    path('get-excel', views.get_excel_function, name='get-excel'),
]
