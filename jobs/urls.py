from django.urls import path

from jobs import views

app_name='jobs'

urlpatterns = [
    path('', views.jobs, name='jobs'),
    path('job/<str:pk>/', views.job, name='job'),
    path('job-create/', views.createJob, name='job-create'),
    path('job-update/<str:pk>/', views.updateJob, name='job-update'),
    path('job-delete/<str:pk>/', views.deleteJob, name='job-delete'),


    path('job-applications/<str:pk>/', views.createApplyJobview, name='job-applications'),
    path('all-applicant/', views.allApplicantsView, name='all-applicant'),
    path('job-applicant/', views.applicantView, name='job-applicant'),
    path('applied-applicant/<str:pk>/', views.appliedApplicantsView, name='applied-applicant'),
]