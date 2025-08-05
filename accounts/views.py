from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему!')
                    return redirect('profile')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Пользователь не найден.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('login')

