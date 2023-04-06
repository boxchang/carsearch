from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'bases/info.html', locals())


@login_required
def history(request):
    return render(request, 'bases/history.html', locals())

