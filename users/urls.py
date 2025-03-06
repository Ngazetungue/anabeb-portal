from django.urls import path
from django.contrib.auth.views import ( 
    LogoutView,
    
)
from users import views
from .views import CustomRegistrationView, CustomLoginView, profile, logout_user

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
]