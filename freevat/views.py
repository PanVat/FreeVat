from django.shortcuts import render

# Domovská stránka
def index(request):
    return render(request, 'index.html')