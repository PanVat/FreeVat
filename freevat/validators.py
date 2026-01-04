import os
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Název modelu (pouze písmena, čísla, mezery a podtržítka, 3-50 znaků)
def validate_model_name(value):
    if not re.match(r'^[\w ]+$', value):
        raise ValidationError(_("can only contain letters, numbers, and _"))
    if len(value) < 3 or len(value) > 50:
        raise ValidationError(_("must be 3-50 characters long"))


# Model (max 100 MB)
def validate_model_file_size(value):
    limit = 100 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_("file is too large (max 100 MB)"))


# Obrázek (max 2 MB)
def validate_image_file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_("image is too large (max 2 MB)"))


# Přípona modelu
def validate_model_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.obj', '.fbx', '.stl', '.gltf', '.glb', '.blend', '.c4d', '.max', '.3ds', '.mb', '.ma']
    if ext not in valid_extensions:
        raise ValidationError(_("unsupported 3D model format"))
