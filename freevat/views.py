from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .forms import ModelUploadForm  # Formulář pro nahrání modelu
from .models import Model3D, ModelImage, Category  # Tabulky z databáze


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
def model_list(request, category_name=None):
    # Základní QuerySet (zatím bez řazení)
    models = Model3D.objects.all()
    current_category = None

    # Filtrování podle kategorie
    if category_name:
        # Najdeme kategorii v databázi podle názvu
        current_category = get_object_or_404(Category, name=category_name)
        # Vyfiltrujeme pouze modely patřící do této kategorie
        models = models.filter(category=current_category)

    # Řazení podle zvoleného kritéria
    sort_by = request.GET.get('sort', 'newest')

    # Nejnovější
    if sort_by == 'newest':
        models = models.order_by('-id')
    # Nejstarší
    elif sort_by == 'oldest':
        models = models.order_by('id')
    # Vzestupně podle názvu
    elif sort_by == 'name_asc':
        models = models.order_by('name')
    # Sestupně podle názvu
    elif sort_by == 'name_desc':
        models = models.order_by('-name')
    else:
        # Fallback pro případ neznámého parametru
        models = models.order_by('-id')

    # Předání dat do šablony
    return render(request, 'model_list.html', {
        'models': models,
        'current_category': current_category,
        'current_sort': sort_by
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
