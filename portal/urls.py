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

    # List view for Members and Guards
    path('members/', views.member_list, name='member_list'),
    path('guards/', views.guard_list, name='guard_list'),

    # Add views for creating Members and Guards
    path('add/member/', views.add_member, name='add_member'), 
    path('add/guard/', views.add_guard, name='add_guard'),

    # Edit views for updating Members and Guards
    path('edit/member/<int:id>/', views.edit_member, name='edit_member'),
    path('edit/guard/<int:id>/', views.edit_guard, name='edit_guard'),

    # Delete views for Members and Guards
    path('delete/member/<int:id>/', views.delete_member, name='delete_member'),
    path('delete/guard/<int:id>/', views.delete_guard, name='delete_guard'),
]
