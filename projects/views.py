from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def projects(request):
    projects = Project.objects.all()
    content = {'projects': projects}
    return render(request, 'projects/projects.html', content)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    content = {'project': projectObj}
    return render(request, 'projects/project.html', content)


@login_required(login_url='login')
def project_create(request):
    profile = request.user.profile
    # Need to create project 
    form = ProjectForm
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    content = {'form': form}
    return render(request, 'projects/project_form.html', content)


@login_required(login_url='login')
def project_update(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    content = {'form': form}
    return render(request, 'projects/project_form.html', content)


@login_required(login_url='login')
def project_delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    content = {'object': project}
    return render(request, 'delete_template.html', content)
