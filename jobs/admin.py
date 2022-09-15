from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(JobModel)
admin.site.register(ApplicantModel)
admin.site.register(TagModel)
