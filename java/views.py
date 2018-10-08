from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from radiusadmin.models import Radcheck

import requests
import json


@csrf_exempt
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        voucher_code = request.POST['voucher_code']
        client_mac = request.session['client_mac']
        try:
            radcheck = Radcheck.objects.get(
                mac_address=client_mac,
                organization='java-voucher')
            radcheck.value = voucher_code
            radcheck.save()
        except Radcheck.DoesNotExist:
            radcheck = Radcheck(username=client_mac + voucher_code,
                                attribute='Cleartext-Password',
                                op=':=',
                                value=voucher_code,
                                mac_address=client_mac,
                                organization='java-voucher')
            radcheck.save()

        radcheck = Radcheck.objects.get(value=voucher_code)
        login_url = request.session['login_url']
        success_url = 'http://' + request.get_host() + \
            reverse('java:welcome')
        login_params = {"username": radcheck.username,
                        "password": radcheck.value,
                        "success_url": success_url}
        r = requests.post(login_url, params=login_params)
        return HttpResponseRedirect(r.url)
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

    return render(request, 'java/index.html')


def welcome(request):
    # logout_url = request.GET.get('logout_url', '')
    # continue_url = 'https://www.google.com/'
    context = {
        'browse_url': 'https://www.google.com/',
    }
    return render(request, 'java/welcome.html', context)
