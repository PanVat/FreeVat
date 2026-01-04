from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Submit
from .models import Category, Comment

# Validátory
from .validators import (
    validate_model_name,
    validate_model_file_size,
    validate_image_file_size,
    validate_model_extension
)

# CSS třídy pro vstupy do formulářových polí a popisy
INPUT_CLASSES = "form-input-classes"
LABEL_CLASSES = "form-label-classes"


# Nahrání formuláře s 3D modelem
class ModelUploadForm(forms.Form):
    # Název modelu
    model_name = forms.CharField(
        max_length=50,
        min_length=3,
        validators=[validate_model_name],
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
        required=False,
        validators=[validate_model_file_size, validate_model_extension],
        label=_('Model'),
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.obj,.fbx,.stl,.gltf,.glb,.blend,.c4d,.max,.3ds,.mb,.ma'
        })
    )

    # Náhledový obrázek
    preview_image = forms.ImageField(
        required=True,
        validators=[validate_image_file_size],
        label=_('Thumbnail'),
        widget=forms.FileInput(attrs={
            'class': 'file-input hidden',
            'accept': '.jpg,.jpeg,.png,.webp'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        other_category = Category.objects.filter(name='Other').first()
        if other_category:
            self.fields['category'].initial = other_category

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.form_id = 'uploadForm'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.label_class = LABEL_CLASSES

        # 1. Globální vypnutí chyb pod poli
        self.helper.form_show_errors = False

        # 2. Definice layoutu s explicitním vypnutím chyb u každého pole
        self.helper.layout = Layout(
            Field('model_name', css_class=INPUT_CLASSES, show_errors=False),
            Field('description', css_class=INPUT_CLASSES, show_errors=False),
            Field('model_file', show_errors=False),
            Field('preview_image', show_errors=False),
            # Pole 'category' je HiddenInput, takže chyby obvykle neukazuje,
            # ale pro jistotu ho můžeš přidat taky:
            Field('category', show_errors=False),

            Submit('submit', _('Upload Model'), css_class="form-submit-button")
        )


# Uživatelský komentář k 3D modelu
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-[#2A2A2A] text-white p-4 rounded-md focus:outline-none text-base',
                'placeholder': _('Write a comment...'),
                'rows': '3',
            }),
        }
