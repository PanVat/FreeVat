from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .forms import ModelUploadForm
from .models import Model3D, ModelImage


# Domovská stránka
def index(request):
    return render(request, 'index.html')


# Nahrání 3D modelu (je potřeba být přihlášen)
@login_required(login_url='login')
def upload_model(request):
    if request.method == 'POST':
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Vytvoření hlavního modelu
            # (Používáme commit=False, abychom mohli přidat uživatele před uložením,
            # pokud bys používal ModelForm, u Form jen vytvoříme instanci)
            data = form.cleaned_data

            new_model = Model3D(
                name=data['model_name'],
                category=data['category'],  # Přidání vybrané kategorie
                description=data['description'],
                model=data['model_file'],
                thumbnail=data['preview_image'],
                user=request.user
            )
            new_model.save()

            # 2. Zpracování GALERIE (více souborů)
            # request.FILES.getlist() je klíčové pro získání všech nahraných fotek
            images = request.FILES.getlist('gallery_images')
            for f in images:
                ModelImage.objects.create(
                    model_3d=new_model,
                    image=f
                )

            return redirect('index')
    else:
        form = ModelUploadForm()

    return render(request, 'upload.html', {'form': form})


# Zobrazení živatelského profilu (pouze pro přihlášené)
@login_required
def user_profile(request):
    return render(request, 'users/profile.html')


# Detail 3D modelu
def model_detail(request, pk):
    # Najde model podle Primary Key (ID), nebo vrátí chybu 404
    model_obj = get_object_or_404(Model3D, pk=pk)

    context = {
        'model': model_obj,
        'debug': settings.DEBUG  # Zde předáme proměnnou do šablony
    }
    return render(request, 'model_detail.html', context)


def model_list(request):
    models = Model3D.objects.all().order_by('-id')

    return render(request, 'model_list.html', {'models': models})
