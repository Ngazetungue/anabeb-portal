from django import forms
from .models import Guard, Member

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
