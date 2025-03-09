from django.contrib import admin
from .models import Guard, Member

@admin.register(Guard)
class GuardAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'identification_document', 'date_of_birth', 'age',
        'cellphone_number', 'village_assigned', 'date_employed', 'status'
    )
    search_fields = ('first_name', 'last_name', 'identification_document')
    list_filter = ('gender', 'status', 'village_assigned')
    ordering = ('last_name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'identification_document', 'date_of_birth', 'age', 
         'date_join', 'status', 'date_deceased', 'membership_period', 'cellphone_number', 'village'
    )
    search_fields = ('first_name', 'last_name', 'identification_document')
    list_filter = ('status', 'village')
    ordering = ('last_name',)