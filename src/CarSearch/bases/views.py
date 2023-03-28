from django.shortcuts import render


def index(request):
    return render(request, 'bases/info.html', locals())


def history(request):
    return render(request, 'bases/history.html', locals())

