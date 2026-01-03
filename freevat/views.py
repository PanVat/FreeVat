from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .forms import ModelUploadForm, CommentForm  # Formulář pro nahrání modelu
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
            # Vytvoření modelu
            new_model = Model3D.objects.create(
                name=form.cleaned_data['model_name'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                model=form.cleaned_data['model_file'],
                thumbnail=form.cleaned_data['preview_image'],
                user=request.user
            )

            # Zpracování galerie
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                ModelImage.objects.create(
                    model3d=new_model,
                    image=f
                )

            # Po úspěšném nahrání přesměrování na domovskou stránku
            return redirect('index')
    else:
        form = ModelUploadForm()

    # Vykreslení domovské stránky
    return render(request, 'forms/upload.html', {'form': form})


# Zobrazení živatelského profilu (pouze pro přihlášené)
@login_required
def user_profile(request):
    # Načtení modelů, které patří přihlášenému uživateli
    user_models_preview = Model3D.objects.filter(user=request.user).order_by('-id')[:8]

    return render(request, 'users/profile.html', {
        'user_models': user_models_preview,
        'total_models_count': Model3D.objects.filter(user=request.user).count(),
    })


# Pomocná funkce pro sjednocení logiky řazení
def get_sorted_models(queryset, request):
    sort_by = request.GET.get('sort', 'newest')

    if sort_by == 'oldest':
        return queryset.order_by('id'), sort_by
    elif sort_by == 'name_asc':
        return queryset.order_by('name'), sort_by
    elif sort_by == 'name_desc':
        return queryset.order_by('-name'), sort_by
    else:
        # Výchozí: nejnovější
        return queryset.order_by('-id'), 'newest'


# Zobrazení všech modelů uživatele
@login_required
def user_models_list(request):
    # Fetchujeme všechny modely přihlášeného uživatele
    models = Model3D.objects.filter(user=request.user)

    # Použití sjednocené logiky řazení
    models, current_sort = get_sorted_models(models, request)

    # Vrácení šablony a dat
    return render(request, 'users/user_models_all.html', {
        'models': models,
        'current_sort': current_sort
    })


# Smazání modelu
@login_required
def delete_model(request, pk):
    model_obj = get_object_or_404(Model3D, pk=pk, user=request.user)
    if request.method == 'POST':
        model_obj.delete()
        return redirect('user_models_all')
    return redirect('user_models_all')


# Úprava již nahraného modelu
@login_required
def edit_model(request, pk):
    model_obj = get_object_or_404(Model3D, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Ruční aktualizace polí
            model_obj.name = form.cleaned_data['model_name']
            model_obj.category = form.cleaned_data['category']
            model_obj.description = form.cleaned_data['description']

            # Aktualizace souborů pouze, pokud byly nahrány
            if 'model_file' in request.FILES:
                model_obj.model = request.FILES['model_file']
            if 'preview_image' in request.FILES:
                model_obj.thumbnail = request.FILES['preview_image']

            model_obj.save()

            # Zpracování galerie
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                ModelImage.objects.create(model3d=model_obj, image=f)

            # Smazání obrázků z galerie
            delete_ids = request.POST.get('delete_images', '').split(',')
            for img_id in delete_ids:
                if img_id.strip().isdigit():
                    ModelImage.objects.filter(id=img_id, model3d=model_obj).delete()

            # Přesměrování
            return redirect('user_models_all')
        else:
            print(form.errors)
    else:
        initial_data = {
            'model_name': model_obj.name,
            'category': model_obj.category,
            'description': model_obj.description,
        }
        form = ModelUploadForm(initial=initial_data)

    return render(request, 'forms/edit_model.html', {
        'form': form,
        'model': model_obj
    })


# Seznam nahraných 3D modelů
def model_list(request, category_name=None, format_ext=None, software_name=None):
    models = Model3D.objects.all()
    current_filter = None

    # Filtrování podle kategorie
    if category_name:
        category_obj = get_object_or_404(Category, name=category_name)
        models = models.filter(category=category_obj)
        current_filter = category_obj.name

    # Filtrování podle formátu
    elif format_ext:
        models = models.filter(data__file_format__iexact=format_ext)
        current_filter = format_ext.upper()

    # Filtrování podle softwaru
    elif software_name:
        models = models.filter(data__file_format__iexact=software_name)
        current_filter = software_name

    # Použití sjednocené logiky řazení
    models, current_sort = get_sorted_models(models, request)

    # Výpis stránky
    return render(request, 'models/model_list.html', {
        'models': models,
        'current_filter': current_filter,
        'current_sort': current_sort,
    })


# Detail 3D modelu
def model_detail(request, pk):
    model_obj = get_object_or_404(Model3D, pk=pk)

    # Zpracování nového komentáře (pokud je uživatel přihlášen)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Autor je aktuálně přihlášený uživatel
            comment.model3d = model_obj  # Komentář patří k tomuto modelu
            comment.save()
            return redirect('model_detail', pk=pk)  # Refresh stránky po odeslání
    else:
        form = CommentForm()

    # Načtení galerie a podobných modelů
    gallery = model_obj.images.all()
    similar_models = Model3D.objects.filter(category=model_obj.category).exclude(pk=pk)[:3]

    # Načtení komentářů pro tento konkrétní model
    comments = model_obj.comments.all()

    # Předání dat do šablony
    context = {
        'model': model_obj,
        'gallery': gallery,
        'similar_models': similar_models,
        'comments': comments,
        'comment_form': form,
        'debug': settings.DEBUG
    }
    return render(request, 'models/model_detail.html', context)
