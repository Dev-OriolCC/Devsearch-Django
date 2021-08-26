from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    content = { 'form': form }
    return render(request, 'projects/project_form.html', content)

def project_update(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    content = {'form': form}
    return render(request, 'projects/project_form.html', content)

def project_delete(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    content = {'object': project}
    return render(request, 'projects/delete_template.html', content)




