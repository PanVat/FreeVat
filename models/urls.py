from django.urls import path
from . import views

app_name = 'freevat'

urlpatterns = [
    path('', views.index, name='index'),
]