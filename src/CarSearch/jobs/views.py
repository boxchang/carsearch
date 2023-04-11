from django.http import Http404
from django.shortcuts import render

from jobs.models import FileJob


def detail(request):
    try:
        jobs = FileJob.objects.all()

    except FileJob.DoesNotExist:
        raise Http404('Job does not exist')


    return render(request, 'jobs/detail.html', locals())


def delete(request, batch_no):
    try:
        job = FileJob.objects.get(batch_no=batch_no)
        job.delete()
        jobs = FileJob.objects.all()
    except FileJob.DoesNotExist:
        raise Http404('Job does not exist')

    return render(request, 'jobs/detail.html', locals())