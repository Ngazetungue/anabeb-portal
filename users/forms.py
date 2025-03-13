from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Profile


class CustomRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
 
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'cellphone_number','first_name','last_name','sex','date_of_birth','password1', 'password2', 'user_type', 'status' ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'cellphone_number',]

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
