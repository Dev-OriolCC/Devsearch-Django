import os

from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utilities import searchProfiles, paginateProfiles

# Create your views here.
def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    content = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
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
        username = request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
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
            return redirect('editAccount')
        else:
            messages.error(request, 'Error during register')
    return render(request, 'users/login_register.html', content)


def logoutUser(request):
    messages.success(request, 'You have logged out.')
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def accountUser(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    content = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', content)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        if request.FILES:
            if profile.profile_image.name != 'profiles/default-profile.jpg':
                file = 'C:/Users/cesar/PycharmProjects/devsearch/static/images/' + profile.profile_image.name
                os.remove(file)

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # if request.FILES:
            #     file = 'C:/Users/cesar/PycharmProjects/devsearch/static/images/profiles/'+profile.profile_image.name
            #     os.remove(file)
            #     form.save()
            form.save()
            return redirect('account')

    content = {'form': form}
    return render(request, 'users/profile_form.html', content)


@login_required(login_url='login')
def skill_create(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    content = {'form': form}
    return render(request, 'users/skill_form.html', content)


@login_required(login_url='login')
def skill_update(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    content = {'form': form}
    return render(request, 'users/skill_form.html', content)


@login_required(login_url='login')
def skill_delete(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    content = {'object': skill}
    return render(request, 'delete_template.html', content)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messagesProfile = profile.messages.all()
    messagesUnread = messagesProfile.filter(is_read=False).count()
    content = {'messagesProfile': messagesProfile, 'messagesUnread': messagesUnread}
    return render(request, 'users/inbox.html', content)


@login_required(login_url='login')
def message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    content = {'message': message}
    return render(request, 'users/message.html', content)


def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('profile', pk=recipient.id)

    content = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', content)
