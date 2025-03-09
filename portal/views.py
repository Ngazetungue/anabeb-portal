from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Guard, Member
from .forms import GuardForm, MemberForm

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/staff/staff-dashboard.html'

    
class AdminDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'portal/admin/admin-dashboard.html'

# STAFF DASHBOARD
# Guard

# List all guards
def guard_list(request):
    guards = Guard.objects.all()
    return render(request, 'portal/staff/staff_list_guard.html', {'guards': guards})

# Add a new guard
def add_guard(request):
    if request.method == 'POST':
        form = GuardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guard_list')
    else:
        form = GuardForm()
    return render(request, 'portal/staff/staff_create_guard.html', {'form': form})

# Edit a guard
def edit_guard(request, pk):
    guard = get_object_or_404(Guard, pk=pk)
    if request.method == 'POST':
        form = GuardForm(request.POST, instance=guard)
        if form.is_valid():
            form.save()
            return redirect('guard_list')
    else:
        form = GuardForm(instance=guard)
    return render(request, 'portal/staff/staff_update_guard.html', {'form': form, 'guard': guard})

# Delete a guard
def delete_guard(request, pk):
    guard = get_object_or_404(Guard, pk=pk)
    if request.method == 'POST':
        guard.delete()
        return redirect('guard_list')
    return render(request, 'portal/staff/staff_delete_guard.html', {'guard': guard})

# Member

# View to list all members
def member_list(request):
    members = Member.objects.all()
    return render(request, 'portal/staff/staff_list_member.html', {'members': members})

# View to add a new member
def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'portal/staff/staff_create_member.html', {'form': form})

# View to edit an existing member
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'portal/staff/staff_update_member.html', {'form': form, 'member': member})

# View to delete a member
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == "POST":
        member.delete()
        return redirect('member_list')
    return render(request, 'portal/staff/staff_delete_member.html', {'member': member})
