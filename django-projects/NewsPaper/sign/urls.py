from django.urls import path
from .views import IndexView, BaseRegisterView, upgrade_me
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html')),
    path('upgrade/', upgrade_me, name='upgrade')
]
