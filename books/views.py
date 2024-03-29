from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Book, Comment
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


def book_detail_view(request, pk, slug):
    book = get_object_or_404(Book, pk=pk, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_object = form.save(commit=False)
            comment_object.author = request.user
            comment_object.book = book
            try:
                comment_object.parent = form.cleaned_data['parent']
            except:
                comment_object.parent = None
            form.save()
        return render(request, 'books/book_detail.html', {'form': form, 'book': book})

    else:
        form = CommentForm()
        return render(request, 'books/book_detail.html', {'form': form, 'book': book})


class SearchResultView(generic.ListView):
    model = Book
    template_name = 'books/book_search_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query)
        )
        return object_list
