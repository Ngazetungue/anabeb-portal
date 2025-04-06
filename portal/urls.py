from django.urls import path
from .views import (
    StaffDashboardView, AdminDashboardView,
)

from . import views

app_name = 'portal'

urlpatterns = [
    # Dashboards
    path('staff-dashboard/', StaffDashboardView.as_view(), name='staff-dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

    path('staff/', views.staff_list, name='staff_list'),
    path('detail/staff/<int:id>/', views.staff_detail, name='staff_detail'),
    path('update/staff/<int:id>/', views.staff_update, name='staff_update'),
    path('delete/staff/<int:id>/', views.staff_delete, name='staff_delete'),

    # List view for Members and Guards
    path('members/', views.member_list, name='member_list'),
    path('guards/', views.guard_list, name='guard_list'),

    # Details view for Members and Guards
    path('members/<int:id>/', views.member_detail, name='member_detail'),
    path('guards/<int:id>/', views.guard_detail, name='guard_detail'),

    # Add views for creating Members and Guards
    path('add/member/', views.add_member, name='add_member'), 
    path('add/guard/', views.add_guard, name='add_guard'),

    # Edit views for updating Members and Guards
    path('edit/member/<int:id>/', views.edit_member, name='edit_member'),
    path('edit/guard/<int:id>/', views.edit_guard, name='edit_guard'),

    # Delete views for Members and Guards
    path('delete/member/<int:id>/', views.delete_member, name='delete_member'),
    path('delete/guard/<int:id>/', views.delete_guard, name='delete_guard'),

    path('create-payslip/', views.create_payslip, name='create_payslip'),
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslip/update/<int:pk>/', views.payslip_update, name='payslip_update'),
    path('payslip/<int:payslip_id>/', views.payslip_detail, name='payslip_detail'),
    path('payslip/delete/<int:pk>/', views.payslip_delete, name='payslip_delete'),
    path('payslip/download/<int:payslip_id>/', views.payslip_download_pdf, name='payslip_download_pdf'),
]
