from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Radcheck
from .generate import TOTPVerification

import requests
import json

totp_verification = TOTPVerification()


@csrf_exempt
def index(request):
    message = ''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        voucher_code = request.POST['voucher_code']
        phone_number = request.POST['phone_number']

        voucher_url = 'http://178.62.86.105/validate'
        voucher_params = {
            "code": voucher_code
        }
        voucher_r = requests.post(
            voucher_url,
            params=voucher_params)
        parsed_json = json.loads(voucher_r.text)
        message = parsed_json['message']

        if message == 'success':
            try:
                radcheck = Radcheck.objects.get(username=phone_number)
                updated_token = totp_verification.generate_token()
                radcheck.value = updated_token
                radcheck.code = voucher_code
                radcheck.save()

                headers = {'Content-type': 'application/json'}
                sms_url = 'http://pay.brandfi.co.ke:8301/sms/send'
                welcome_message = 'Online access code is: ' + updated_token
                sms_params = {
                    "clientId": "2",
                    "message": welcome_message,
                    "recepients": phone_number
                }
                sms_r = requests.post(
                    sms_url,
                    json=sms_params,
                    headers=headers)
            except Radcheck.DoesNotExist:
                generated_token = totp_verification.generate_token()
                headers = {'Content-type': 'application/json'}
                radcheck = Radcheck(username=phone_number,
                                    attribute='Cleartext-Password',
                                    op=':=',
                                    value=generated_token,
                                    code=voucher_code)
                radcheck.save()

                sms_url = 'http://pay.brandfi.co.ke:8301/sms/send'
                welcome_message = 'Online access code is: ' + generated_token
                sms_params = {
                    "clientId": "2",
                    "message": welcome_message,
                    "recepients": phone_number
                }
                sms_r = requests.post(
                    sms_url,
                    json=sms_params,
                    headers=headers)
            return HttpResponseRedirect(reverse('radiusadmin:verify'))
        else:
            context = {
                'message': message,
            }
            return render(request, 'radiusadmin/index.html',  context)
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

        context = {
            'message': message,
        }
    return render(request, 'radiusadmin/index.html',  context)


@csrf_exempt
def verify(request):
    status = ''
    if request.method == 'POST':
        password = request.POST['password']

        try:
            radcheck = Radcheck.objects.get(value=password)

            valid_url = 'http://178.62.86.105/update'
            valid_params = {"code": radcheck.code,
                            "additional_info": radcheck.username}
            valid_r = requests.post(
                valid_url,
                params=valid_params)

            print(valid_r.status_code)

            login_url = request.session['login_url']
            success_url = 'http://' + request.get_host() + \
                reverse('radiusadmin:welcome')
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
    return render(request, 'radiusadmin/verify.html', context)


def welcome(request):
    # logout_url = request.GET.get('logout_url', '')
    # continue_url = 'https://www.google.com/'
    context = {
        'browse_url': 'https://www.google.com/',
    }
    return render(request, 'radiusadmin/welcome.html', context)
