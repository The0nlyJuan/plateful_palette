from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from .forms import UserRegisterForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('food:home')
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})

@login_required
def user_logout(request):
    auth_logout(request)
    request.session['just_logged_out'] = True
    return redirect('guest:home')
