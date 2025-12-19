from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout
from django.contrib.auth.forms import PasswordChangeForm

# Pro překlad textů
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Vstupní pole ve formuláři
INPUT_CLASSES = "form-input-classes"

# Třídy pro labely ve formuláři
LABEL_CLASSES = "text-lg font-medium mb-2 block"


## Formulář pro registraci ##
class CustomUserCreationForm(UserCreationForm):
    # Uživatelské jméno
    username = forms.CharField(
        max_length=50,
        label=_("Username"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your username')
        }),
    )

    # Email
    email = forms.EmailField(
        max_length=254,
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your email')
        }),
    )

    # Heslo
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your password')
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Odstranění pole pro potvrzení hesla
        del self.fields['password2']

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        self.helper.form_show_errors = False  # Skryje chyby napsané pod vstupní pole

        # Nastavíme třídy pro labely
        self.helper.label_class = LABEL_CLASSES

        # Vlastní layout
        self.helper.layout = Layout(
            Field('username', css_class=INPUT_CLASSES),
            Field('email', css_class=INPUT_CLASSES),
            Field('password1', css_class=INPUT_CLASSES),
            Submit('submit', _("Sign up"))
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Email address is already in use."))
        return email


class CustomLoginForm(forms.Form):
    # Email místo username
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your email')
        }),
    )

    # Heslo
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your password')
        }),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        self.helper.label_class = LABEL_CLASSES

        # Vlastní layout pro login
        self.helper.layout = Layout(
            Field('email', css_class=INPUT_CLASSES),
            Field('password', css_class=INPUT_CLASSES),
            Submit('submit', _("Log in"))
        )

    # Validace emailu a hesla
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Najdi uživatele podle emailu
            try:
                user = User.objects.get(email=email)
                # Authenticate pomocí username
                user = authenticate(username=user.username, password=password)
                if user is None:
                    raise forms.ValidationError(_("Invalid email or password."))
            except User.DoesNotExist:
                raise forms.ValidationError(_("Invalid email or password."))
        return cleaned_data


# users/forms.py
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'website_url']  # Přidáno website_url
        widgets = {
            # Uživatelské jméno
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': _('Your username')
            }),
            # Email
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': _('Your email')
            }),
            # Bio/Popis uživatele
            'bio': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 4,
                'placeholder': _('Tell us something about yourself')
            }),
            # Odkaz na webovou stránku nebo portfolio
            'website_url': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': _('Your web or portfolio link')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = LABEL_CLASSES
        self.helper.form_show_errors = False
        self.fields['email'].label = _("Email")
        self.fields['email'].required = True

        self.helper.layout = Layout(
            Field('username', css_class=INPUT_CLASSES),
            Field('email', css_class=INPUT_CLASSES),
            Field('website_url', css_class=INPUT_CLASSES),  # Umístěno nad Bio
            Field('bio', css_class=INPUT_CLASSES),
        )


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Definice placeholderů pro jednotlivá pole
        placeholders = {
            'old_password': _('Your current password'),
            'new_password1': _('Your new password'),
            'new_password2': _('Confirm new password'),
        }

        # Projdeme všechna pole a nastavíme jim vlastnosti
        for field_name, field in self.fields.items():
            # Skrytí help_textu
            field.help_text = None

            # Nastavení placeholderu z našeho slovníku
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

            # Aplikace tvé CSS třídy pro ohraničení
            field.widget.attrs.update({'class': INPUT_CLASSES})

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = LABEL_CLASSES
        self.helper.form_show_errors = False

        # Přepsání labelů na kratší verzi
        self.fields['old_password'].label = _("Current password")
        self.fields['new_password1'].label = _("New password")
        self.fields['new_password2'].label = _("Confirm new password")

         # Vlastní layout
        self.helper.layout = Layout(
            *[Field(field, css_class=INPUT_CLASSES) for field in self.fields]
        )
