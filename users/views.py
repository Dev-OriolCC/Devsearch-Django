from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    content = {'profiles': profiles}
    return render(request, 'users/profiles.html', content)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    content = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/profile.html', content)


def loginPage(request):
    page = 'login'
    # Block login page for auth users
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check if username exists in db.
        try:
            user = User.objects.get(username=username)
        except:
            print('Username was not found')
            messages.error(request, 'Username was not found')
        # Check if username & passwords are correct
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
                messages.error(request, 'Credentials are wrong')
    content = {'page': page}
    return render(request, 'users/login_register.html', content)


def registerUser(request):
    form = CustomUserCreationForm()
    page = 'register'
    content = {'page': page, 'form': form}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account has been created successfully')
            # Finally login the new user
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Error during register')
    return render(request, 'users/login_register.html', content)


def logoutUser(request):
    messages.success(request, 'You have logged out.')
    logout(request)
    return redirect('login')
