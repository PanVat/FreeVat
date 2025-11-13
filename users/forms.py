from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout

# Pro překlad textů
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Vstupní pole ve formuláři
INPUT_CLASSES = "block w-full px-3 py-2 border-2 custom-input-border placeholder-gray-400"

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

    # Potvrzení hesla
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Confirm your password')
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'  # Přidá mezeru mezi poli

        # Nastavíme třídy pro labely
        self.helper.label_class = LABEL_CLASSES

        # Vlastní CSS styly pro pole formuláře
        self.helper.layout = Layout(
            Field('username', css_class=INPUT_CLASSES),
            Field('email', css_class=INPUT_CLASSES),
            Field('password1', css_class=INPUT_CLASSES),
            Field('password2', css_class=INPUT_CLASSES),
            Submit('submit', _("Sign up"),
                   css_class="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-medium")
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Email address is already in use."))
        return email


class CustomLoginForm(forms.Form):
    # Uživatelské jméno
    username = forms.CharField(
        max_length=150,
        label=_("Username"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': _('Enter your username')
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
        self.helper.form_class = 'space-y-4'  # Přidá mezeru mezi poli
        self.helper.label_class = LABEL_CLASSES  # Aplikujeme třídy na labely

        # Tlačítko pro přihlášení
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            Submit('submit', _("Log in"),
                   css_class="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-medium")
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(_("Invalid username or password."))
        return cleaned_data
