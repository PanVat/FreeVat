from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .forms import ModelUploadForm  # Formulář pro nahrání modelu
from .models import Model3D, ModelImage  # Tabulky z databáze
from .models import Category, Format, Software  # Tabulky z databáze


# Domovská stránka
def index(request):
    # Načtení všech kategorií
    categories = Category.objects.all().order_by('name')

    # Načtení 10 nejnovějších modelů
    latest_models = Model3D.objects.all().order_by('-id')[:8]

    # Předání dat do šablony
    context = {
        'categories': categories,
        'latest_models': latest_models
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
def model_list(request, category_name=None, format_ext=None, software_name=None):
    models = Model3D.objects.all()
    current_filter = None

    # 1. Filtrování podle kategorie
    if category_name:
        category_obj = get_object_or_404(Category, name=category_name)
        models = models.filter(category=category_obj)
        current_filter = category_obj.name

    # 2. Filtrování podle formátu
    elif format_ext:
        models = models.filter(data__file_format__iexact=format_ext)
        current_filter = format_ext.upper()

    # 3. Filtrování podle softwaru (přes příponu v Data)
    elif software_name:
        models = models.filter(data__file_format__iexact=software_name)
        current_filter = software_name


    # Řazení
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        models = models.order_by('-id')
    elif sort_by == 'oldest':
        models = models.order_by('id')

    # Výpis stránky
    return render(request, 'model_list.html', {
        'models': models,
        'current_filter': current_filter,
        'current_sort': sort_by,
    })


# Detail 3D modelu
def model_detail(request, pk):
    model_obj = get_object_or_404(Model3D, pk=pk)

    # Načtení galerie obrázků pro tento model
    gallery = model_obj.images.all()  # Předpokládám related_name='images' v ModelImage

    # Načtení podobných modelů (stejná kategorie, kromě aktuálního)
    similar_models = Model3D.objects.filter(category=model_obj.category).exclude(pk=pk)[:3]

    context = {
        'model': model_obj,
        'gallery': gallery,
        'similar_models': similar_models,
        'debug': settings.DEBUG
    }
    return render(request, 'model_detail.html', context)
