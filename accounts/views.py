from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm


@login_required
def edit_profile_view(request):

    form = ProfileForm(request.POST or None, request.FILES, instance=request.user)

    if form.is_valid():
        form.save()

    return render(request, 'accounts/profile.html', {'form': form})
