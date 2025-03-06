from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/staff/staff-dashboard.html'

    
class AdminDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'portal/admin/admin-dashboard.html'

    
# ADMIN DASHBOARD
# Staff 
def staff_create(request):
    return render(request, "portal/home.html")

def staff_update(request):
    return render(request, "portal/home.html")

def staff_view(request):
    return render(request, "portal/home.html")

def staff_delete(request):
    return render(request, "portal/home.html")

def home(request):
    return render(request, "portal/home.html")

# Villages
def village_create(request):
    return render(request, "portal/home.html")

def village_update(request):
    return render(request, "portal/home.html")

def village_view(request):
    return render(request, "portal/home.html")

def village_delete(request):
    return render(request, "portal/home.html")

# STAFF DASHBOARD
# Guard

def guard_create(request):
    return render(request, "portal/home.html")

def guard_update(request):
    return render(request, "portal/home.html")

def guard_view(request):
    return render(request, "portal/home.html")

def guard_delete(request):
    return render(request, "portal/home.html")

# Member
def member_create(request):
    return render(request, "portal/home.html")

def member_update(request):
    return render(request, "portal/home.html")

def member_view(request):
    return render(request, "portal/home.html")

def member_delete(request):
    return render(request, "portal/home.html")