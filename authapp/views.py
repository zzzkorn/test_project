from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import RespondentUserLoginForm, RespondentUserRegisterForm, RespondentUserChangeForm


def login(request):
    title = 'вход'
    next_url = request.GET['next'] if 'next' in request.GET.keys() else ''
    # next_url = request.GET.get('next', '')
    login_form = RespondentUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.GET.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))
    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = RespondentUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            # Создать пользователя
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = RespondentUserRegisterForm()
    content = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = RespondentUserChangeForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            # Создать пользователя
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = RespondentUserChangeForm(instance=request.user)
    content = {
        'title': title,
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', content)

