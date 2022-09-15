from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *

def homeView(request):
    return render(request,'home.html')


def registerEmployerView(request):
    form = CustomUserCretionForm()

    if request.method == 'POST':
        form=CustomUserCretionForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_employer = True
            user.is_employee = False
            user.email=user.email.lower()
            user.save()

            return redirect('user:account')

    context = {'form': form}
    return render(request, 'account/employerSignup.html', context)


@login_required(login_url='account_login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()

    context = {'profile': profile, 'skills': skills}
    return render(request, 'users/account.html', context)


@login_required(login_url='account_login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def userProfile(request, pk):
    profile = ProfileModel.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/profile.html', context)


@login_required(login_url='account_login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Başarıyla eklendi!')
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='account_login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, 'Beceri başarıyla güncellendi!')
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='account_login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Beceri başarıyla silindi!')
        return redirect('users:account')

    context = {'object': skill}
    return render(request, 'users/skill_delete.html', context)


@login_required(login_url='account_login')
def inbox(request):
    profile = request.user.profile

    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='account_login')
def viewMessage(request, pk):
    profile = request.user.profile

    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = ProfileModel.objects.get(id=pk)
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
                message.name = sender.user.first_name
                message.email = sender.user.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('users:user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
