from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import ipware
import requests
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
import datetime
import string
from random import choice
from django.conf import settings


def generate_random_string(length):
    letters = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
    rand_string = ''.join(choice(letters) for i in range(length))
    return rand_string


def index(request, last):
    try:
        found = Links.objects.get(name=last)
        ip = ipware.get_client_ip(request)
        if ip[1]:
            ip_info = requests.get(f"https://geolocation-db.com/json/{ip[0]}&position=true").json()
            ip_info = f"{ip_info['country_name']}, {ip_info['city']}"
        else:
            ip_info = 'localhost'
        req_data = Passes()
        req_data.link, req_data.owner_link, req_data.ip, req_data.region = last, found.owner, ip[0], ip_info
        req_data.save()
        found.counter += 1
        found.save()
        if found.screamer:
            return render(request, 'screamer.html')
        else:
            return HttpResponseRedirect(found.redirect)

    except ObjectDoesNotExist:
        return HttpResponse('Ссылка не существует!')


def none_page(request):
    return HttpResponseRedirect('/login')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/profile')
        else:
            messages.error(request, 'Ошиба авторизации')
    else:
        form = UserLoginForm
    context = {'form': form}
    return render(request, 'login.html', context=context)


def profile_view(request):
    if request.method == 'POST':
        create_data_pro = ShortMyLinkPro(request.POST)
        if create_data_pro.is_valid():
            try:
                Links.objects.get(name=create_data_pro.cleaned_data['name'])
                messages.error(request, 'Такая ссылка уже существует!')
            except ObjectDoesNotExist:
                if create_data_pro.cleaned_data['name'] == 'None':
                    addr = generate_random_string(8)
                else:
                    addr = create_data_pro.cleaned_data['name']
                new_link = Links()
                new_link.name, new_link.redirect, new_link.screamer, new_link.owner = \
                    addr, \
                    create_data_pro.cleaned_data['redirect'], \
                    create_data_pro.cleaned_data['screamer'], \
                    request.user.username
                new_link.save()
                messages.success(request, settings.LINK + addr)

    if request.user.is_authenticated:
        if request.user.is_superuser:
            status = 'admin'
            form_add = ShortMyLinkPro
        else:
            try:
                user_profile = Profiles.objects.get(nickname=request.user.username)
                if datetime.datetime.now() > user_profile.sub_till.replace(tzinfo=None):
                    status = 'default'
                    form_add = ShortMyLink
                else:
                    status = 'pro'
                    form_add = ShortMyLinkPro
            except ObjectDoesNotExist:
                status = 'default'
                form_add = ShortMyLink
        passes = (Passes.objects.filter(owner_link=request.user.username)).order_by('-time')
        context = {
            'status': status,
            'form_add': form_add,
            'passes': passes
        }
        return render(request, 'profile.html', context=context)
    else:
        return HttpResponseRedirect('/login')
