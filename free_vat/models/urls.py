from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.models, name='models'),
]