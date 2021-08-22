from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('projects/<int:number>', views.project, name="project"),
]