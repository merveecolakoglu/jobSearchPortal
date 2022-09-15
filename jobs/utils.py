from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateJobs(request,jobs,results):
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(jobs, results)

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        jobs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        jobs = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range,jobs


def searchJobs(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = TagModel.objects.filter(name__icontains=search_query)

    jobs = JobModel.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query)|
        Q(tags__in=tags)
    )

    return jobs, search_query
