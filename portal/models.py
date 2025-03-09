from django.db import models
from django.core.validators import RegexValidator
from datetime import date

class Guard(models.Model):
    SEX = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    USER_STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    VILLAGE_ASSIGNED = [
        ("anabeb", "Anabeb"),
        ("otjondunda", "Otjondunda"),
        ("ombaikiha", "Ombaikiha"),
        ("warmquelle", "Warmquelle"),
        ("khowarib", "Khowarib"),
        ("omukutu", "Omukutu"),
        ("otjondumbu", "Otjondumbu"),
        ("okaturua", "Okaturua"),
        ("otjatjondjira", "Otjatjondjira"),
    ]

    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=SEX, default="male")
    identification_document = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{1,15}$",
                "Identification number must contain only digits and be up to 15 digits long.",
            )
        ],
    )
    date_of_birth = models.DateField(null=True, blank=True)
    cellphone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{1,15}$",
                "Phone number must contain only digits and be up to 15 digits long.",
            )
        ],
    )
    village_assigned = models.CharField(
        max_length=50, choices=VILLAGE_ASSIGNED, default="warmquelle"
    )
    date_employed = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default="active")

    def __str__(self):
        return self.first_name

    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None

        