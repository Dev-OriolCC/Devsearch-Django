from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:id>', views.project, name="project"),
]