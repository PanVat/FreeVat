from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Domovská stránka
def index(request):
    return render(request, 'index.html')

@login_required
def upload_model(request):
    return render(request, 'users/upload.html')

@login_required
def user_profile(request):
    return render(request, 'users/profile.html')