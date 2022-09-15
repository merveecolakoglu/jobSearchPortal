from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model
from .forms import *
# Create your views here.
from .utils import *


def jobs(request):
    jobs, search_query = searchJobs(request)
    custom_range, jobs = paginateJobs(request, jobs, 6)

    context = {'jobs': jobs, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'jobs/jobs.html', context)


def job(request, pk):
    job = JobModel.objects.get(id=pk)
    tags = job.tags.all()

    return render(request, 'jobs/job.html', {'job': job, 'tags': tags})


@login_required(login_url='account_login')
def createJob(request):
    profile = request.user.profile
    form = JobForm()

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            job.owner = profile
            job.save()

            return redirect('jobs:jobs')

    context = {'form': form}
    return render(request, 'jobs/job_form.html', context)


@login_required(login_url='account_login')
def updateJob(request, pk):
    profile=request.user.profile
    job = profile.jobmodel_set.get(id=pk)
    form = JobForm(instance=job)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()

            return redirect('jobs:jobs')

    context = {'form': form}
    return render(request, 'jobs/job_form.html', context)


@login_required(login_url='account_login')
def deleteJob(request, pk):
    profile=request.user.profile
    job = profile.jobmodel_set.get(id=pk)

    if request.method == 'POST':
        job.delete()
        return redirect('jobs:jobs')

    context = {'job': job}
    return render(request, 'jobs/job-delete.html', context)


@login_required(login_url='account_login')
def createApplyJobview(request, pk):
    form = ApplyJobForm(request.POST or None)
    profile = get_object_or_404(ProfileModel, id=request.user.profile.pk)
    applicant = ApplicantModel.objects.filter(user=profile, job=pk)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = profile
                instance.save()
                return redirect('jobs:jobs')
        else:
            return redirect('jobs:jobs')

    context = {'applicant': applicant, 'form': form}
    return render(request, 'jobs/job.html', context)


@login_required(login_url='account_login')
def allApplicantsView(request):
    applicants = ApplicantModel.objects.all()

    context = {'applicants': applicants}
    return render(request, 'jobs/all_applicant.html', context)


@login_required(login_url='account_login')
def applicantView(request):
    profile = request.user.profile
    applicant = profile.applicants.all()

    context = {'applicant': applicant}
    return render(request, 'jobs/job_applicant.html', context)


@login_required(login_url='account_login')
def appliedApplicantsView(request, pk):
    applicant = ApplicantModel.objects.get(id=pk)

    if applicant.is_read == False:
        applicant.is_read = True
        applicant.save()

    context = {'applicant': applicant}
    return render(request, 'jobs/applied_applicant.html', context)
