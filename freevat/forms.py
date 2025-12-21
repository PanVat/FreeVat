from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.utils.translation import gettext_lazy as _ # Překlad
from .models import Category

# CSS třídy pro vstupy do formulářových polí a popisy
INPUT_CLASSES = "form-input-classes"
LABEL_CLASSES = "form-label-classes"


class ModelUploadForm(forms.Form):

    # Název modelu
    model_name = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
        label=_('Name'),
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter model name')
        })
    )

    # Kategorie
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label=_('Category'),
        widget=forms.HiddenInput()
    )

    # Popis modelu
    description = forms.CharField(
        required=False,
        max_length=1000,
        min_length=10,
        label=_('Description'),
        widget=forms.Textarea(attrs={
            'class': INPUT_CLASSES + ' min-h-[150px] resize-y',
            'placeholder': _('Describe your model...')
        })
    )

    # Samotný 3D model
    model_file = forms.FileField(
        required=True,
        label=_('Model'),
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.obj,.fbx,.stl,.gltf,.glb,.usdz,.blend,.c4d,.max,.3ds,.mb,.ma'
        })
    )

    # Náhledový obrázek
    preview_image = forms.ImageField(
        required=True,
        label=_('Thumbnail'),
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.jpg,.jpeg,.png,.webp'
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