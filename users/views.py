from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomLoginForm

# Registrace uživatele přes uživatelský formulář
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# Přihlášení uživatele přes uživatelský formulář
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = CustomLoginForm()

    return render(request, 'users/login.html', {'form': form})


# Odhlášení uživatele
def logout_view(request):
    logout(request)
    return redirect('index')
