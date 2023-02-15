from django.shortcuts import reverse, get_object_or_404, redirect
from django.http import HttpResponse
from orders.models import Order
import requests
import json


def payment_process(request):
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': 'Put your merchant id :)',
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.first_name} {order.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),

    }
    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()['data']
    authority = data['authority']

    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback(reqeust):
    payment_authority = reqeust.GET.get('Authority')
    payment_status = reqeust.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': 'Put your merchant id :)',
            'amount': rial_total_price,
            'authority': payment_authority,

        }

        response = requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json',
                                 data=json.dumps(request_data),
                                 headers=request_header)

        if 'data' in response.json()\
                and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0):
            data = response.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('Successfully paid :)')

            elif payment_code == 101:
                return HttpResponse('This transaction is pay before :(')

            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return HttpResponse(f'Not successfully :(  {error_code} {error_message}')

    else:
        return HttpResponse('Not successfully :(')


def payment_process_sandbox(request):
    # get order id from session
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'MerchantID': 'abcABCabcABCabcABCabcABCabcABCabcABC',
        'Amount': rial_total_price,
        'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        # 'callback_url': 'http://127.0.0.1:8000' + reverse('payment:payment_callback'),
        'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()
    print(data)
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        print(response.json())
        return HttpResponse('errors from zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }

        request_data = {
            'MerchantID': 'abcABCabcABCabcABCabcABCabcABCabcABC',
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }

        response = requests.post(url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
                                 data=json.dumps(request_data),
                                 headers=request_header)
        print(response.json())
        if 'errors' not in response.json():
            data = response.json()
            payment_cod = data['Status']

            if payment_cod == 100:
                order.is_paid = True
                order.ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_cod == 101:
                return HttpResponse('البته این تراکنش قبلا ثبت شده است')

            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return HttpResponse(f'{error_code}{error_message} تراکنش ناموفق بود /:')

    else:
        return HttpResponse(f'تراکنش ناموفق بود /:')
