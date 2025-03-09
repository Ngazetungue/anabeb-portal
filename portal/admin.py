from django.contrib import admin
from .models import Guard

@admin.register(Guard)
class GuardAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'identification_document', 'date_of_birth', 'age',
        'cellphone_number', 'village_assigned', 'date_employed', 'status'
    )
    search_fields = ('first_name', 'last_name', 'identification_document')
    list_filter = ('gender', 'status', 'village_assigned')
    ordering = ('last_name',)
