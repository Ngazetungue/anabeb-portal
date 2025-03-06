from django.urls import path
from .views import (
    home,
     StaffDashboardView, AdminDashboardView,
)

app_name = 'portal'
urlpatterns = [
    path('', home, name='home'),

    # Dashboards
    path('staff-dashboard/', StaffDashboardView.as_view(), name='staff-dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]