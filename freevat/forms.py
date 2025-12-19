from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Category

INPUT_CLASSES = "form-input-classes"
LABEL_CLASSES = "form-label-classes"


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ModelUploadForm(forms.Form):
    # Název modelu - Povinné (required=True)
    model_name = forms.CharField(
        max_length=200,
        required=True,
        label='Name',
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter model name'
        })
    )

    # Kategorie - Povinné s výchozí hodnotou
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='Category',
        widget=forms.HiddenInput()
    )

    description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.Textarea(attrs={
            'class': INPUT_CLASSES + ' min-h-[150px] resize-y',
            'placeholder': 'Describe your model...'
        })
    )

    # Soubor modelu - Povinné (required=True)
    model_file = forms.FileField(
        required=True,
        label='Model',
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.obj,.fbx,.stl,.gltf,.glb,.usdz,.blend,.c4d,.max,.3ds,.mb,.ma'
        })
    )

    # Náhledový obrázek - Změněno na Povinné (required=True)
    preview_image = forms.ImageField(
        required=True,
        label='Thumbnail',
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.jpg,.jpeg,.png,.webp'
        })
    )

    gallery_images = forms.FileField(
        required=False,
        label='Gallery',
        widget=MultipleFileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.jpg,.jpeg,.png,.webp',
            'multiple': True
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Nastavení výchozí hodnoty pro kategorii "Other"
        other_category = Category.objects.filter(name='Other').first()
        if other_category:
            self.fields['category'].initial = other_category

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.form_id = 'uploadForm'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.label_class = LABEL_CLASSES
        self.helper.layout = Layout(
            Submit('submit', 'Upload Model')
        )

    def clean_model_file(self):
        model_file = self.cleaned_data.get('model_file')
        if model_file:
            max_size = 500 * 1024 * 1024
            if model_file.size > max_size:
                raise forms.ValidationError('File size exceeds the maximum limit of 500MB')

            allowed_extensions = ['.obj', '.fbx', '.blend', '.stl', '.gltf', '.glb']
            import os
            file_extension = os.path.splitext(model_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f'File type {file_extension} is not supported')
        return model_file

    def clean_preview_image(self):
        preview_image = self.cleaned_data.get('preview_image')
        if preview_image:
            max_size = 10 * 1024 * 1024
            if preview_image.size > max_size:
                raise forms.ValidationError('Preview image size exceeds 10MB')
        return preview_image
