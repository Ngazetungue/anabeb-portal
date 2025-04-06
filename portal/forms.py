from django import forms
from .models import Guard, Member, Payslip

class GuardForm(forms.ModelForm):
    class Meta:
        model = Guard
        fields = [
            'first_name', 'last_name', 'gender', 'identification_document', 'date_of_birth',
            'cellphone_number', 'village_assigned','status'
        ]

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'gender', 'identification_document', 'date_of_birth',
            'cellphone_number', 'village', 'date_join', 'status', 'date_deceased'
        ]

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = [
            'guard', 'basic_salary', 'hours_worked', 'overtime_hours', 
            'bonus', 'allowances', 'deductions'
        ]
        widgets = {
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control'}),
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowances': forms.NumberInput(attrs={'class': 'form-control'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_overtime_hours(self):
        overtime_hours = self.cleaned_data.get('overtime_hours')
        if overtime_hours < 0:
            raise forms.ValidationError("Overtime hours cannot be negative.")
        return overtime_hours

    def clean_basic_salary(self):
        basic_salary = self.cleaned_data.get('basic_salary')
        if basic_salary <= 0:
            raise forms.ValidationError("Basic salary must be greater than zero.")
        return basic_salary
