from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path
from client_app.views import main_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='chat'),
    re_path(r'^accounts/login/$', 
        LoginView.as_view(
            template_name='login.html'
        ), 
        name="login"
    ),
    re_path(r'^accounts/logout/$', 
        LogoutView.as_view(
            template_name='index.html'
        ), 
        name="logout"
    ),
]
