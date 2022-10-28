from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.AboutUsPageView.as_view(), name='about'),
]