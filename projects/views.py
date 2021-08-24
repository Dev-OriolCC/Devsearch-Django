from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    content = { 'projects': projects }
    return render(request, 'projects/projects.html', content)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    content = { 'project': projectObj}
    return render(request, 'projects/project.html', content)

def project_create(request):
    # Need to create project 
    form = ProjectForm
    content = { 'form': form }
    return render(request, 'projects/project_form.html', content)





