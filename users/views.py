import random
import io
from PIL import Image, ImageDraw, ImageFont

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model


from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm, StyledPasswordChangeForm

User = get_user_model()


# Vytvoří čtvercový obrázek s iniciálami uživatele na barevném pozadí
def generate_initials_avatar(username):
    # Paleta barev pro pozadí
    colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#16a085', '#27ae60', '#2980b9', '#8e44ad',
              '#2c3e50', '#f1c40f', '#e67e22', '#e74c3c', '#95a5a6', '#f39c12', '#d35400', '#c0392b']
    bg_color = random.choice(colors)

    size = 200  # Velikost v pixelech
    image = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Získání iniciál (max 2 písmena)
    initials = username[:2].upper()

    # Pokus o načtení fontu
    try:
        # Cesta k fontu
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Vycentrování textu
    try:
        left, top, right, bottom = draw.textbbox((0, 0), initials, font=font)
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
        # Starší verze Pillow
        text_width, text_height = draw.textsize(initials, font=font)

    x = (size - text_width) / 2
    y = (size - text_height) / 2 - 5  # Drobná korekce výšky

    draw.text((x, y), initials, fill='white', font=font)

    # Uložení do paměti
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{username}_default.png')


# Registrace uživatele
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Uložíme uživatele
            user = form.save(commit=False)

            # Vygenerujeme defaultní fotku
            avatar_file = generate_initials_avatar(user.username)
            user.picture.save(f'{user.username}_avatar.png', avatar_file, save=False)

            # Definitivně uložíme uživatele
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Účet pro {user.username} byl vytvořen!')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'forms/register.html', {'form': form})


# Piřhlášení uživatele
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Najdeme uživatele podle emailu
            try:
                target_user = User.objects.get(email=email)
                user = authenticate(request, username=target_user.username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('index')
            except User.DoesNotExist:
                messages.error(request, 'Neplatný email nebo heslo.')
    else:
        form = CustomLoginForm()
    return render(request, 'forms/login.html', {'form': form})


# Odhlášení uživatele
def logout_view(request):
    logout(request)
    return redirect('index')


# Úprava profilu uživatele
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Váš profil byl aktualizován!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'forms/edit_profile.html', {'form': form})


# Změna hesla uživatele
@login_required
def change_password(request):
    if request.method == 'POST':
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Důležité: udrží uživatele přihlášeného
            update_session_auth_hash(request, user)
            messages.success(request, 'Vaše heslo bylo úspěšně změněno!')
            return redirect('profile')
    else:
        form = StyledPasswordChangeForm(request.user)
    return render(request, 'forms/change_password.html', {'form': form})
