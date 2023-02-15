from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    # path('process/', views.payment_process, name='payment_process'),
    # path('callback/', views.payment_callback, name='payment_callback'),
    path('process/', views.payment_process_sandbox, name='payment_process'),
    path('callback/', views.payment_callback_sandbox, name='payment_callback'),
]
