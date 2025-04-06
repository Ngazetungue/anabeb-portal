from django.contrib import admin
from .models import Guard, Member, Payslip, CompanyInfo

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

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ("guard", "company", "basic_salary", "overtime_pay", "tax", "net_pay", "date_issued")
    list_filter = ("guard__village_assigned",)
    search_fields = ("guard__first_name", "guard__last_name")
    readonly_fields = ("overtime_pay", "tax", "net_pay", "date_issued")
    fieldsets = (
        ("Guard Information", {
            "fields": ("guard", "company", "date_issued"),
        }),
        ("Salary Details", {
            "fields": ("basic_salary", "hours_worked", "overtime_hours", "overtime_pay", "bonus", "allowances", "deductions"),
        }),
        ("Final Calculation", {
            "fields": ("tax", "net_pay"),
        }),
    )

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'email', 'website']

admin.site.register(CompanyInfo, CompanyInfoAdmin)
