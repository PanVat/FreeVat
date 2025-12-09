import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import ModelUploadForm
from .models import Model3D  # Import modelu, pokud ho máš


# Domovská stránka
def index(request):
    return render(request, 'index.html')


@login_required
def upload_model(request):
    """Stránka pro upload 3D modelů pomocí Crispy Forms"""

    if request.method == 'POST':
        form = ModelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Uložit model do databáze
                model = form.save(commit=False)

                # Nastavit uživatele
                model.user = request.user
                model.author_name = request.user.get_full_name() or request.user.username

                # Zpracovat preview image pokud existuje
                preview_image = form.cleaned_data.get('preview_image')
                if preview_image:
                    # Uložit preview image
                    fs_preview = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'previews'))
                    preview_filename = fs_preview.save(preview_image.name, preview_image)
                    model.preview_image = fs_preview.url(preview_filename)

                # Uložit 3D model soubor (už by měl být uložen přes form.save())
                # Ale pojďme to udělat explicitně pro jistotu
                model_file = form.cleaned_data.get('model_file')
                if model_file:
                    fs_model = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, '3d_models'))
                    model_filename = fs_model.save(model_file.name, model_file)
                    model.model_file = model_filename

                # Uložit model do databáze
                model.save()

                # Pokud používáš ManyToMany pole (např. tags), ulož je teď
                if hasattr(model, 'tags') and 'tags' in form.cleaned_data:
                    tags = form.cleaned_data['tags']
                    # Zpracovat tags podle potřeby
                    # Například: model.tags.add(*tags.split(','))

                messages.success(request,
                                 '🎉 3D model has been uploaded successfully! It will be reviewed by our team and published soon.')
                return redirect('upload')

            except Exception as e:
                messages.error(request, f'Error uploading file: {str(e)}')
                # Znovu zobrazit formulář s chybou
                return render(request, 'upload.html', {'form': form})
        else:
            # Zobraz chyby z validace formuláře
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"{field_name}: {error}")

    else:
        # GET request - vytvoř prázdný formulář
        form = ModelUploadForm()

    # DŮLEŽITÉ: Předat form do contextu!
    return render(request, 'upload.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'users/profile.html')