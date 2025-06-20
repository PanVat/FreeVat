from django.shortcuts import render
from django.http import HttpResponse

# 
def models(request):
    return HttpResponse("This is the models page.")
