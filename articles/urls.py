from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # Create
    path('create/', views.create, name='create'),
    # Read
    path('', views.index, name='index'),
    path('<int:id>', views.detail, name='detail'),
    # Update
    path('<int:id>/update/', views.update, name='update'),
    # Delete
    path('<int:id>/delete/', views.delete, name='delete'),
]