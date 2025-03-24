from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # Create
    path('create/', views.create, name='create'),
    # Read

    # Update

    # Delete
]