from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>', views.project, name="project"),
    path('project-create', views.project_create, name="project_create"),
]