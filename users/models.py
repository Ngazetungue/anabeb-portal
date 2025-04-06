from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from datetime import date

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    USER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='staff')
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    identification_document = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Identification number must contain only digits and be up to 15 digits long.')]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX, default="male")
    cellphone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Phone number must contain only digits and be up to 15 digits long.')]
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='staff')
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='active')
    date_join = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    employment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
    
    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None

class Profile(models.Model):
    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    USER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, blank=True)
    cellphone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Phone number must contain only digits and be up to 15 digits long.')]
    )
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    identification_document = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{1,15}$', 'Identification number must contain only digits and be up to 15 digits long.')]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX, default="male")
    user_type = models.CharField(max_length=10, choices=CustomUser.USER_TYPE_CHOICES, default='staff')
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='active')
    date_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None
