from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .forms import ModelUploadForm
from .models import Model3D, ModelImage, Category


# Domovská stránka
def index(request):
    # Načtení všech kategorií
    categories = Category.objects.all().order_by('name')

    context = {
        'categories': categories
    }

    return render(request, 'index.html', context)


# Nahrání 3D modelu (je potřeba být přihlášen)
@login_required(login_url='login')
def upload_model(request):
    if request.method == 'POST':
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Vytvoření modelu
            new_model = Model3D.objects.create(
                name=form.cleaned_data['model_name'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                model=form.cleaned_data['model_file'],
                thumbnail=form.cleaned_data['preview_image'],
                user=request.user
            )

            # 2. Zpracování galerie
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                ModelImage.objects.create(
                    model3d=new_model,
                    image=f
                )

            # 3. Po úspěšném nahrání přesměrování na domovskou stránku
            return redirect('index')
    else:
        form = ModelUploadForm()

    return render(request, 'upload.html', {'form': form})


# Zobrazení živatelského profilu (pouze pro přihlášené)
@login_required
def user_profile(request):
    return render(request, 'users/profile.html')


# Seznam nahraných 3D modelů
def model_list(request, category_name=None):
    models = Model3D.objects.all().order_by('-id')
    current_category = None

    if category_name:
        # Najdeme kategorii v databázi podle názvu
        current_category = get_object_or_404(Category, name=category_name)
        # Vyfiltrujeme pouze modely patřící do této kategorie
        models = models.filter(category=current_category)

    return render(request, 'model_list.html', {
        'models': models,
        'current_category': current_category
    })


# Detail 3D modelu
def model_detail(request, pk):
    model_obj = get_object_or_404(Model3D, pk=pk)
    context = {
        'model': model_obj,
        'debug': settings.DEBUG
    }
    return render(request, 'model_detail.html', context)
