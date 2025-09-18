from django.shortcuts import render
from django.utils.translation import gettext as _ # Pro překlad do jiných jazyků
from django.utils.translation import get_language, activate, gettext

# Domovská stránka
def index(request):
    return render(request, 'index.html')