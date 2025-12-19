from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm, StyledPasswordChangeForm


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


# Úprava profilu uživatele
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Váš profil byl aktualizován!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


# Změna hesla uživatele
@login_required
def change_password(request):
    if request.method == 'POST':
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Důležité: udrží uživatele přihlášeného
            messages.success(request, 'Vaše heslo bylo úspěšně změněno!')
            return redirect('profile')
    else:
        form = StyledPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})
