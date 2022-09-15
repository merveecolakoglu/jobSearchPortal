from django.db import models
import uuid
# Create your models here.
from users.models import ProfileModel

class TagModel(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class JobModel(models.Model):
    owner = models.ForeignKey(ProfileModel, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to='jobs/%Y/%m/', default='default.jpg')
    type_choices = [("1", "Full Time"), ("2", "Part Time"), ("3", "Internship")]
    type = models.CharField(choices=type_choices, default=False, max_length=10)
    tags = models.ManyToManyField(TagModel, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Jobs'
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url =self.featured_image.url
        except:
            url =''
        return url

    def __str__(self):
        return self.title


class ApplicantModel(models.Model):
    user = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, blank=True, null=True,related_name='applicants')
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Applicants'
        unique_together = [['user', 'job']]
        ordering = ['is_read','-created']

    def __str__(self):
        return str(self.user.user.get_full_name())
