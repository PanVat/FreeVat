import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Uživatelské jméno (pouze písmena, čísla a podtržítka, max 20 znaků)
def validate_username(value):
    if len(value) > 20:
        raise ValidationError(_("max 20 characters"))

    if not re.match(r'^[\w]+$', value):
        raise ValidationError(
            _("can only contain letters, numbers, and _")
        )


# Uživatelské heslo (minimálně 6 znaků, alespoň 1 číslice)
def validate_password(value):
    if len(value) < 6:
        raise ValidationError(_("minimum 6 characters"))

    if not re.search(r'\d', value):
        raise ValidationError(_("must contain at least one digit"))
