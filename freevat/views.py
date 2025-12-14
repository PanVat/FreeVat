from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ModelUploadForm
from .models import Model3D


# Domovská stránka
def index(request):
    return render(request, 'index.html')


# Nahrání 3D modelu (je potřeba být přihlášen)
@login_required(login_url='login')
def upload_model(request):
    if request.method == 'POST':
        # Načtení dat z formuláře včetně souborů (request.FILES)
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Získání vyčištěných dat z formuláře
            data = form.cleaned_data

            # Vytvoření instance Model3D (ještě se neukládá do DB)
            new_model = Model3D(
                name=data['model_name'],
                description=data['description'],
                model=data['model_file'],
                thumbnail=data['preview_image'],
                user=request.user  # Přiřazení aktuálně přihlášeného uživatele
            )

            # Uložení modelu do databáze
            new_model.save()

            # Po úspěšném nahrání přesměrování na domovskou stránku (index.html)
            return redirect('index')

    else:
        # GET request - prázdný formulář
        form = ModelUploadForm()

    # Zobrazení formuláře pro nahrání modelu
    return render(request, 'upload.html', {'form': form})


# Zobrazení živatelského profilu (pouze pro přihlášené)
@login_required
def user_profile(request):
    return render(request, 'users/profile.html')
