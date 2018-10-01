from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RadcheckSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from .models import Radcheck
from .generate import TOTPVerification

import requests

totp_verification = TOTPVerification()


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        try:
            radcheck = Radcheck.objects.get(username=phone_number)
            updated_token = totp_verification.generate_token()
            radcheck.value = updated_token
            radcheck.save()

            headers = {'Content-type': 'application/json'}
            sms_url = 'http://pay.brandfi.co.ke:8301/sms/send'
            welcome_message = 'Welcome, your access code to get online is ' + \
                updated_token
            sms_params = {
                "clientId": "2",
                "message": welcome_message,
                "recepients": phone_number
            }
            request.session['phone_number'] = phone_number
            sms_r = requests.post(sms_url, json=sms_params, headers=headers)
        except Radcheck.DoesNotExist:
            generated_token = totp_verification.generate_token()
            headers = {'Content-type': 'application/json'}
            radcheck = Radcheck(username=phone_number,
                                attribute='Cleartext-Password',
                                op=':=',
                                value=generated_token)
            radcheck.save()

            sms_url = 'http://pay.brandfi.co.ke:8301/sms/send'
            welcome_message = 'Welcome, your access code to get online is ' + \
                generated_token
            sms_params = {
                "clientId": "2",
                "message": welcome_message,
                "recepients": phone_number
            }
            request.session['phone_number'] = phone_number
            sms_r = requests.post(sms_url, json=sms_params, headers=headers)
        return HttpResponseRedirect(reverse('radiusadmin:verify'))
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
    return render(request, 'radiusadmin/index.html')


def verify(request):
    if request.method == 'POST':
        password = request.POST['password']

        username = request.session['phone_number']
        radcheck = Radcheck.objects.get(username=username)

        if password == radcheck.value:
            login_url = request.session['login_url']
            success_url = 'http://' + request.get_host() + \
                reverse('radiusadmin:welcome')
            login_params = {"username": username,
                            "password": password,
                            "success_url": success_url}
            r = requests.post(login_url, params=login_params)
            return HttpResponseRedirect(r.url)
        else:
            print("Denied")
    return render(request, 'radiusadmin/verify.html')


def welcome(request):
    return render(request, 'radiusadmin/welcome.html')
