from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
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