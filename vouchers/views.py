from django.shortcuts import render
from django.views.generic import View
from .render import Render
from django.http import HttpResponse
from django.urls import reverse

import requests
import json
import pdfkit


def index(request):
    download_url = 'http://' + request.get_host() + \
        reverse('vouchers:download-vouchers')
    context = {
        'download_url': download_url,
    }
    return render(request, 'vouchers/index.html', context)


def download_vouchers(request):
    # Use False instead of output path to save pdf to a variable
    generate_url = 'http://' + request.get_host() + \
        reverse('vouchers:generate-codes')
    pdf = pdfkit.from_url(generate_url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vouchers.pdf"'

    return response


def generate_codes(request):
    voucher_url = 'http://178.62.86.105/gen_codes'
    voucher_params_1 = {"numbers": 4}
    voucher_params_2 = {"numbers": 4}
    voucher_params_3 = {"numbers": 4}
    voucher_params_4 = {"numbers": 4}
    voucher_params_5 = {"numbers": 4}
    voucher_params_6 = {"numbers": 4}
    voucher_params_7 = {"numbers": 4}
    voucher_params_8 = {"numbers": 4}
    voucher_params_9 = {"numbers": 4}
    r_1 = requests.get(voucher_url, params=voucher_params_1)
    r_2 = requests.get(voucher_url, params=voucher_params_2)
    r_3 = requests.get(voucher_url, params=voucher_params_3)
    r_4 = requests.get(voucher_url, params=voucher_params_4)
    r_5 = requests.get(voucher_url, params=voucher_params_5)
    r_6 = requests.get(voucher_url, params=voucher_params_6)
    r_7 = requests.get(voucher_url, params=voucher_params_7)
    r_8 = requests.get(voucher_url, params=voucher_params_8)
    r_9 = requests.get(voucher_url, params=voucher_params_9)
    voucher_codes_1 = json.loads(r_1.text)
    voucher_codes_2 = json.loads(r_2.text)
    voucher_codes_3 = json.loads(r_3.text)
    voucher_codes_4 = json.loads(r_4.text)
    voucher_codes_5 = json.loads(r_5.text)
    voucher_codes_6 = json.loads(r_6.text)
    voucher_codes_7 = json.loads(r_7.text)
    voucher_codes_8 = json.loads(r_8.text)
    voucher_codes_9 = json.loads(r_9.text)

    context = {
        'voucher_codes_1': voucher_codes_1,
        'voucher_codes_2': voucher_codes_2,
        'voucher_codes_3': voucher_codes_3,
        'voucher_codes_4': voucher_codes_4,
        'voucher_codes_5': voucher_codes_5,
        'voucher_codes_6': voucher_codes_6,
        'voucher_codes_7': voucher_codes_7,
        'voucher_codes_8': voucher_codes_8,
        'voucher_codes_9': voucher_codes_9,
    }

    return render(request, 'vouchers/vouchers.html', context)
