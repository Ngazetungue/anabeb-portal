from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date

class Guard(models.Model):
    SEX = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    GUARD_STATUS_CHOICES = [
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

    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=SEX, default="male")
    identification_document = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{1,11}$",
                "Identification number must contain only digits and be up to 11 digits long.",
            )
        ],
    )
    date_of_birth = models.DateField(null=False, blank=False)
    cellphone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{1,15}$",
                "Phone number must contain only digits and be up to 10 digits long.",
            )
        ],
    )
    village_assigned = models.CharField(
        max_length=50, choices=VILLAGE_ASSIGNED, default="warmquelle"
    )
    date_employed = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=GUARD_STATUS_CHOICES, default="alive")

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

class Member(models.Model):
    SEX = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    MEMBER_STATUS_CHOICES = [
        ("alive", "Alive"),
        ("deceased", "Deceased"),
    ]
    VILLAGE = [
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

    first_name = models.CharField(max_length=150, help_text="Enter the member's first name.")
    last_name = models.CharField(max_length=150, help_text="Enter the member's last name.")
    gender = models.CharField(max_length=10, choices=SEX, default="male", help_text="Select the member's gender.")
    identification_document = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                r"^\d{1,11}$",
                "Identification number must contain only digits and be up to 11 digits long.",
            )
        ],
        help_text="Enter the member's identification number (up to 11 digits).",
    )
    date_of_birth = models.DateField(help_text="Enter the member's date of birth.")
    cellphone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r"^\d{1,10}$",
                "Phone number must contain only digits and be up to 10 digits long.",
            )
        ],
        help_text="Enter the member's cellphone number (up to 10 digits).",
    )
    village = models.CharField(
        max_length=50, choices=VILLAGE, default="warmquelle", help_text="Select the member's village."
    )
    date_join = models.DateField(help_text="Enter the date the member joined.")
    status = models.CharField(max_length=10, choices=MEMBER_STATUS_CHOICES, default="alive", help_text="Select the member's status.")
    date_deceased = models.DateField(null=True, blank=True, help_text="Enter the date the member passed away (if applicable).")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.status == "deceased" and not self.date_deceased:
            raise ValidationError({"date_deceased": "Date deceased is required for deceased members."})
        if self.status == "alive" and self.date_deceased:
            raise ValidationError({"date_deceased": "Date deceased should be empty for alive members."})
        if self.date_deceased:
            if self.date_deceased < self.date_of_birth:
                raise ValidationError({"date_deceased": "Date deceased cannot be before date of birth."})
            if self.date_deceased < self.date_join:
                raise ValidationError({"date_deceased": "Date deceased cannot be before join date."})

    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None

    def membership_period(self):
        if self.status == "deceased" and self.date_deceased:
            end_date = self.date_deceased
        else:
            end_date = date.today()
        active_years = end_date.year - self.date_join.year

        if (end_date.month, end_date.day) < (self.date_join.month, self.date_join.day):
            active_years -= 1
        return active_years

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['identification_document'], name='unique_identification_document')
        ]
