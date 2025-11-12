from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages


# Registrace uživatele
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('index')
        else:
            messages.error(request, 'Fix the mistakes in your form.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# Přihlášení uživatele
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'users/login.html', {'form': form})


# Odhlášení uživatele (doporučuji přidat taky)
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')
