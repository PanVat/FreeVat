import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ModelUploadForm
from .models import Model3D


# Domovská stránka
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def upload_model(request):
    if request.method == 'POST':
        # Načteme data z formuláře včetně souborů (request.FILES)
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Získání vyčištěných dat
            data = form.cleaned_data

            # 2. Vytvoření instance Model3D (zatím bez uložení do DB, protože řešíme M2M)
            # Ale protože používáme forms.Form a ne ModelForm, musíme instanci vytvořit ručně:
            new_model = Model3D(
                name=data['model_name'],
                description=data['description'],
                model=data['model_file'],
                thumbnail=data['preview_image'],
                user=request.user  # Přiřadíme aktuálně přihlášeného uživatele
            )

            # 3. Uložení samotného modelu do databáze (získá ID)
            new_model.save()

            # 5. Přesměrování po úspěšném nahrání (např. na domovskou stránku)
            return redirect('index')  # Změňte 'home' na název vašeho view pro hlavní stranu

    else:
        # GET request - prázdný formulář
        form = ModelUploadForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'users/profile.html')
