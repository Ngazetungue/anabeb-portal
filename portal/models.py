from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

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

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=255, default="Anabeb Conservancy")
    postal_address = models.CharField(max_length=255, default="P.O Box 108, Opuwo, Namibia")
    address = models.CharField(max_length=255, default="Warmquelle, Kunene Region, Namibia")
    phone = models.CharField(max_length=20, default="+264 81 123 4567")
    email = models.EmailField(default="info@anabebconservancy.com")
    website = models.URLField(default="http://anabebconservancy.com")
    vat_number = models.CharField(max_length=20, default="1234567890")
    logo = models.ImageField(upload_to='company/logos/', null=True, blank=True)
    stamp = models.ImageField(upload_to='company/stamps/', null=True, blank=True)

    def __str__(self):
        return self.company_name

    @classmethod
    def get_instance(cls):
        """
        Ensures that only one instance exists, and creates it if it doesn't exist.
        """
        instance, created = cls.objects.get_or_create(id=1)
        if created:
            instance.save()
        return instance

    def save(self, *args, **kwargs):
        """
        Ensure only one instance of CompanyInfo exists in the database.
        """
        if not self.id and CompanyInfo.objects.exists():
            raise ValueError("Only one CompanyInfo instance is allowed.")
        super().save(*args, **kwargs)

class Payslip(models.Model):
    TAX_RATE = Decimal('0.15')
    OVERTIME_RATE = Decimal('50.00')

    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name="payslips")
    guard = models.ForeignKey(Guard, on_delete=models.CASCADE, related_name="payslips")
    basic_salary = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Base monthly salary before any deductions or bonuses."
    )
    hours_worked = models.PositiveIntegerField(
        default=160, validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Total hours worked in the month. Default is 160 (full-time)."
    )
    overtime_hours = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Extra hours worked beyond the normal working hours."
    )
    overtime_pay = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0.00,
        help_text="Automatically calculated based on overtime hours and rate."
    )
    bonus = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,
        help_text="Additional earnings (performance bonus, holiday bonus, etc.)."
    )
    allowances = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,
        help_text="Extra allowances (e.g., transport, housing)."
    )
    deductions = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,
        help_text="Deductions (e.g., loans, penalties, or other reductions)."
    )
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False,
        help_text="Automatically calculated 15% tax on basic salary."
    )
    net_pay = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False,
        help_text="Final salary after tax and deductions."
    )
    date_issued = models.DateField(auto_now_add=True, help_text="Date when the payslip was generated.")

    class Meta:
        unique_together = ('guard',)
        ordering = ['-date_issued'] 

    def save(self, *args, **kwargs):
        """
        Auto-calculates:
        - Overtime Pay = Overtime Hours * Overtime Rate (default 50 NAD/hour)
        - Tax = 15% of Basic Salary (rounded to 2 decimal places)
        - Net Pay = Basic Salary + Overtime + Bonus + Allowances - (Deductions + Tax)
        """
        self.overtime_pay = (Decimal(self.overtime_hours) * self.OVERTIME_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.tax = (self.basic_salary * self.TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.net_pay = (
            self.basic_salary + self.overtime_pay + self.bonus + self.allowances - (self.deductions + self.tax)
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payslip for {self.guard.first_name} {self.guard.last_name}"
