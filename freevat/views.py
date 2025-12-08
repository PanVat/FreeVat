import os

from django.contrib.auth.decorators import login_required
from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from freevat import settings


# Domovská stránka
def index(request):
    return render(request, 'index.html')

@login_required
def upload_model(request):
    return render(request, 'users/upload.html')

@login_required
def user_profile(request):
    return render(request, 'users/profile.html')

# Upload
@login_required
def upload_model(request):
    """Stránka pro upload 3D modelů - hlavní upload routa"""

    if request.method == 'POST':
        # Získání dat z formuláře
        model_name = request.POST.get('model_name', '').strip()
        author_name = request.POST.get('author_name', '').strip()
        category = request.POST.get('category', '')
        license_type = request.POST.get('license', '')
        description = request.POST.get('description', '').strip()
        tags = request.POST.get('tags', '').strip()
        polygon_count = request.POST.get('polygon_count', '')

        # Validace
        errors = []
        if not model_name:
            errors.append('Model name is required.')
        if not author_name:
            errors.append('Author name is required.')
        if not category:
            errors.append('Category is required.')
        if not license_type:
            errors.append('License type is required.')
        if not description:
            errors.append('Description is required.')

        # Zpracování souboru
        if 'model_file' in request.FILES:
            model_file = request.FILES['model_file']

            # Kontrola velikosti souboru (max 500MB)
            if model_file.size > 500 * 1024 * 1024:
                errors.append('File size exceeds 500MB limit.')

            # Kontrola přípony
            allowed_extensions = ['.obj', '.fbx', '.blend', '.stl', '.gltf', '.glb']
            file_extension = os.path.splitext(model_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                errors.append(f'File type {file_extension} is not supported.')
        else:
            errors.append('Model file is required.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'upload.html', {
                'model_name': model_name,
                'author_name': author_name,
                'category': category,
                'license': license_type,
                'description': description,
                'tags': tags,
                'polygon_count': polygon_count,
            })

        try:
            # Uložení souboru
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, '3d_models'))
            filename = fs.save(model_file.name, model_file)
            file_url = fs.url(filename)

            # ZDE BY SE DATA ULOŽILA DO DATABÁZE
            # Příklad:
            # Model3D.objects.create(
            #     user=request.user,
            #     name=model_name,
            #     author=author_name,
            #     category=category,
            #     license_type=license_type,
            #     description=description,
            #     tags=tags,
            #     polygon_count=polygon_count if polygon_count else None,
            #     file_path=file_url
            # )

            messages.success(request,
                             '🎉 3D model has been uploaded successfully! It will be reviewed by our team and published soon.')
            return redirect('upload')

        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
            return render(request, 'upload.html', {
                'model_name': model_name,
                'author_name': author_name,
                'category': category,
                'license': license_type,
                'description': description,
                'tags': tags,
                'polygon_count': polygon_count,
            })

    # GET request - zobrazit formulář
    return render(request, 'upload.html')