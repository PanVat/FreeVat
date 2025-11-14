from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout

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
        self.helper.form_show_errors = False # Skryje chyby napsané pod vstupní pole

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