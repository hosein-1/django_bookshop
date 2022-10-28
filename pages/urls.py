from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.AboutUsPageView.as_view(), name='about'),
    path('contactus/', views.ContactUsView.as_view(), name='contact_us')
]