from django.contrib.auth import get_user_model

from django import forms

from django.core.validators import RegexValidator, MaxValueValidator
from datetime import date
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Profile

class CustomRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    USER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    identification_document = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Identification number must contain only digits and be up to 15 digits long.')],
        help_text="Enter your identification number (digits only, up to 15 characters)."
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[MaxValueValidator(limit_value=date.today(), message="Date of birth cannot be in the future.")]
    )
    sex = forms.ChoiceField(choices=SEX_CHOICES, initial='male')
    cellphone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Phone number must contain only digits and be up to 15 digits long.')],
        help_text="Enter your phone number (digits only, up to 15 characters)."
    )
    employment_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[MaxValueValidator(limit_value=date.today(), message="Date of employment cannot be in the future.")]
    )
    status = forms.ChoiceField(choices=USER_STATUS_CHOICES, initial='active')

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'identification_document',
            'date_of_birth',
            'sex',
            'employment_date',
            'cellphone_number',
            'password1',
            'password2',
            'user_type',
            'status',
        ]


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