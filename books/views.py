from django.views import generic
from django.shortcuts import get_object_or_404, render

from .models import Book, Comment
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
