from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def project(request, number):
    return render(request, 'projects/project.html')

def projects(request):
    return render(request, 'projects/projects.html')