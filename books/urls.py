from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    re_path(r'book/(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/$', views.BookDetailView.as_view(), name='book_detail'),
]
