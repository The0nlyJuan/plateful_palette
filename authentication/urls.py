from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication\login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),  # This line includes default auth urls
]
