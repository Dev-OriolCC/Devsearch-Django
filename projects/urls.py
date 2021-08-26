from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>', views.project, name="project"),
    path('project-create', views.project_create, name="project_create"),
    path('project-update/<str:pk>', views.project_update, name="project_update"),
    path('project-delete/<str:pk>', views.project_delete, name="project_delete"),
]