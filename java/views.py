from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from radiusadmin.models import Radcheck
from radiusadmin.generate import TOTPVerification

import requests
import json

totp_verification = TOTPVerification()


@csrf_exempt
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        voucher_code = request.POST['voucher_code']
        client_mac = request.session['client_mac']
        try:
            username = client_mac
            radcheck = Radcheck.objects.get(
                username=username,
                organization='kahawa')
            updated_token = totp_verification.generate_token()
            radcheck.value = updated_token
            radcheck.save()
        except Radcheck.DoesNotExist:
            generated_token = totp_verification.generate_token()
            username = client_mac
            radcheck = Radcheck(username=username,
                                attribute='Cleartext-Password',
                                op=':=',
                                value=generated_token,
                                mac_address=client_mac,
                                organization='kahawa')
            radcheck.save()
        return HttpResponseRedirect(reverse('kahawa:verify'))
    else:
        login_url = request.GET.get('login_url', '')
        continue_url = request.GET.get('continue_url', '')
        ap_name = request.GET.get('ap_name', '')
        ap_mac = request.GET.get('ap_mac', '')
        ap_tags = request.GET.get('ap_tags', '')
        client_ip = request.GET.get('client_ip', '')
        client_mac = request.GET.get('client_mac', '')

        request.session['login_url'] = login_url
        request.session['continue_url'] = continue_url
        request.session['ap_name'] = ap_name
        request.session['ap_mac'] = ap_mac
        request.session['ap_tags'] = ap_tags
        request.session['client_ip'] = client_ip
        request.session['client_mac'] = client_mac

    return render(request, 'kahawa/index.html')


@csrf_exempt
def verify(request):
    if request.method == 'POST':
        password = request.POST['password']

        try:
            radcheck = Radcheck.objects.get(value=password)
            login_url = request.session['login_url']
            success_url = 'http://' + request.get_host() + \
                reverse('kahawa:welcome')
            login_params = {"username": radcheck.username,
                            "password": radcheck.value,
                            "success_url": success_url}
            r = requests.post(login_url, params=login_params)
            return HttpResponseRedirect(r.url)
        except Radcheck.DoesNotExist:
            status = 'error'

    context = {
        'message': status,
    }
    return render(request, 'kahawa/verify.html', context)


def welcome(request):
    # logout_url = request.GET.get('logout_url', '')
    # continue_url = 'https://www.google.com/'
    context = {
        'browse_url': 'https://www.google.com/',
    }
    return render(request, 'kahawa/welcome.html', context)
