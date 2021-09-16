import os

from django.core.files import storage
from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utilities import searchProjects, paginateProjects


# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    # projects = Project.objects.all()
    # Paginator
    custom_range, projects = paginateProjects(request, projects, 6)

    content = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', content)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()\

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        #Update
        projectObj.calculateVotes
        return redirect('project', pk=projectObj.id)


    content = {'project': projectObj, 'form': form}
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
        newTags = request.POST.get('newTags').replace(',', ' ').split()
        # Delete previous image if exits
        if request.FILES:
            os.remove(project.featured_image.path)

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            # Not duplicate a existing Tag
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add()

            return redirect('projects')
    content = {'form': form}
    return render(request, 'projects/project_form.html', content)


@login_required(login_url='login')
def project_delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        os.remove(project.featured_image.path)
        project.delete()
        return redirect('projects')

    content = {'object': project}
    return render(request, 'delete_template.html', content)
