from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
        'id': '1',
        'title': 'Blog',
        'description': 'Fully functional blog website.'
    },
    {
        'id': '2',
        'title': 'Covid-19 Tracker',
        'description': 'Functional website to track covid-19 cases.'
    },
    {
        'id': '3',
        'title': 'Anonymous Forum',
        'description': 'Small forum site.'
    }
]

# Create your views here.
def projects(request):
    _message = 'Welcome back user!'
    content = { 'message': _message, 'projects': projectsList }
    return render(request, 'projects/projects.html', content)

def project(request, id):
    projectObj = None
    for i in projectsList:
        if i['id'] == id:
            projectObj = i
    return render(request, 'projects/project.html', { 'project': projectObj })







