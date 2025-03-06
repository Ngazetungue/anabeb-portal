from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from . forms import CustomRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import CustomUser
from .forms import  StaffProfileForm

class CustomRegistrationView(CreateView):
    template_name = 'portal/admin/signup.html'
    form_class = CustomRegistrationForm
    success_url = '/admin-dashboard/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        user_type = user.user_type
        if user_type == 'staff':
            return redirect('portal:admin-staff_list')
        elif user_type == 'admin':
            return redirect('portal:admin-dashboard')
        else:
            return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        login(self.request, form.get_user())
        user_type = form.get_user().user_type
        if user_type == 'staff':
            return redirect('portal:staff-dashboard')
        elif user_type == 'admin':
            return redirect('portal:admin-dashboard')
        else:
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class StaffDashboardView(View):
    template_name = 'portal/staff-dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    template_name = 'portal/admin-dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@login_required
def profile(request):
    profile = request.user.profile
    user_type = request.user.user_type

    if user_type == 'staff':
        form_class = StaffProfileForm
        template = 'registration/edit_staff_profile.html'
    else:
        form_class = AdminProfileForm
        template = 'registration/edit_admin_profile.html'

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = form_class(instance=profile)
    
    return render(request, template, {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')
