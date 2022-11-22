from django.views import generic
from django.shortcuts import get_object_or_404, render

from .models import Book
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


def book_detail_view(request, pk, slug):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            book_object = form.save(commit=False)
            book_object.author = request.user
            book_object.book = book
            form.save()
        return render(request, 'books/book_detail.html', {'form': form, 'book': book})

    else:
        form = CommentForm()
        return render(request, 'books/book_detail.html', {'form': form, 'book': book})
