from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Guard, Member
from users.models import CustomUser, Profile
from .forms import GuardForm, MemberForm

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/staff/staff-dashboard.html'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        number_of_guards = Guard.objects.all().count()
        number_of_members = Member.objects.all().count()

        staff_member = Profile.objects.all()
        
        context["number_of_guards"] = number_of_guards
        context["number_of_members"] = number_of_members
        context["staff_member"] = staff_member
    
        return context
    
class AdminDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'portal/admin/admin-dashboard.html'

@login_required
def guard_list(request):
    guards = Guard.objects.all()
    paginator = Paginator(guards , 13)
    page_number = request.GET.get('page')
    guards = paginator.get_page(page_number)
    return render(request, 'portal/staff/staff_list_guard.html', {'guards': guards})

@login_required
def guard_detail(request, id):
    guard = get_object_or_404(Guard, id=id)
    return render(request, 'portal/staff/staff_detail_guard.html', {'guard': guard})

@login_required
def add_guard(request):
    if request.method == 'POST':
        form = GuardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal:guard_list')
    else:
        form = GuardForm()
    return render(request, 'portal/staff/staff_create_guard.html', {'form': form})

@login_required
def edit_guard(request, id):
    guard = get_object_or_404(Guard, id=id)
    if request.method == 'POST':
        form = GuardForm(request.POST, instance=guard)
        if form.is_valid():
            form.save()
            return redirect('portal:guard_list')
    else:
        form = GuardForm(instance=guard)
    return render(request, 'portal/staff/staff_update_guard.html', {'form': form, 'guard': guard})

@login_required
def delete_guard(request, id):
    guard = get_object_or_404(Guard, id=id)
    if request.method == 'POST':
        guard.delete()
        return redirect('portal:guard_list')
    return render(request, 'portal/staff/staff_delete_guard.html', {'guard': guard})

@login_required
def member_list(request):
    if request.user.user_type in ["admin", "staff"]:
        members_list = Member.objects.all()
        paginator = Paginator(members_list, 13)
        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        return render(request, 'portal/staff/staff_list_member.html', {'members': members})
    else:
        return HttpResponse("You don't permision to access this page")

@login_required
def member_detail(request, id):
    member = get_object_or_404(Member, id=id)
    return render(request, 'portal/staff/staff_detail_member.html', {'member': member})

@login_required
def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal:member_list')
    else:
        form = MemberForm()
    return render(request, 'portal/staff/staff_create_member.html', {'form': form})

@login_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('portal:member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'portal/staff/staff_update_member.html', {'form': form, 'member': member})

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.user.user_type =="admin":
        if request.method == "POST":
            member.delete()
            return redirect('portal:member_list')
        return render(request, 'portal/staff/staff_delete_member.html', {'member': member})

    else:
        return HttpResponse("Only Admins are allowed to delete")
