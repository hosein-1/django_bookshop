from django.urls import path


urlpatterns = [
    path('', create_order, name='order_create'),
]