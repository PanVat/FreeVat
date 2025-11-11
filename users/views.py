from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages


# Registrace uživatele
def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'users/register.html', {'form': form})
