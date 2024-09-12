from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Grading, Profile


class GradingForm(forms.ModelForm):
    class Meta:
        model = Grading
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получаем данные пользователя
        self.fields['user'].queryset = Profile.objects.select_related('user')
