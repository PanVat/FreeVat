from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

# CSS třídy pro vstupní pole ve formuláři (jsou definovány ve 'forms.css')
INPUT_CLASSES = "form-input-classes"

# CSS třídy pro popisy ve formuláři (jsou definovány ve 'forms.css')
LABEL_CLASSES = "form-label-classes"


# Formulář pro nahrání 3D modelu
class ModelUploadForm(forms.Form):
    # Název modelu
    model_name = forms.CharField(
        max_length=200,
        required=True,
        label='Model Name',
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter model name'
        })
    )

    # Popis modelu
    description = forms.CharField(
        required=True,
        label='Model Description',
        widget=forms.Textarea(attrs={
            'class': INPUT_CLASSES + ' min-h-[150px] resize-y',
            'placeholder': 'Describe your model, including details about textures, polygons, and any special features...'
        })
    )

    # Samotný soubor 3D modelu
    model_file = forms.FileField(
        required=True,
        label='3D Model File',
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.obj,.fbx,.stl,.gltf,.glb,.usdz,.blend,.c4d,.max,.3ds,.mb,.ma'
        })
    )

    # Náhledový obrázek
    preview_image = forms.ImageField(
        required=False,
        label='Preview Image',
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.jpg,.jpeg,.png,.webp'
        })
    )

    # Inicializace formuláře s Crispy Forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.form_id = 'uploadForm'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.label_class = LABEL_CLASSES

        # Jednoduchý layout - HTML bude v šabloně
        self.helper.layout = Layout(
            Submit('submit', 'Upload Model')
        )

    # Validace souboru 3D modelu
    def clean_model_file(self):
        model_file = self.cleaned_data.get('model_file')
        if model_file:
            # Kontrola velikosti souboru (max 500MB)
            max_size = 500 * 1024 * 1024
            if model_file.size > max_size:
                raise forms.ValidationError('File size exceeds the maximum limit of 500MB')

            # Kontrola přípony
            allowed_extensions = ['.obj', '.fbx', '.blend', '.stl', '.gltf', '.glb']
            import os
            file_extension = os.path.splitext(model_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f'File type {file_extension} is not supported')

        return model_file

    # Validace náhledového obrázku
    def clean_preview_image(self):
        preview_image = self.cleaned_data.get('preview_image')
        if preview_image:
            # Kontrola velikosti obrázku (max 10MB)
            max_size = 10 * 1024 * 1024
            if preview_image.size > max_size:
                raise forms.ValidationError('Preview image size exceeds the maximum limit of 10MB')

            # Kontrola přípony
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            import os
            file_extension = os.path.splitext(preview_image.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f'Image type {file_extension} is not supported')

        return preview_image
