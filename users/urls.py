from django.urls import path
from django.contrib.auth.views import ( 
    LoginView, 
    LogoutView,
    
)
from users import views
from .views import SignupPageView

urlpatterns = [
    
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    
]
