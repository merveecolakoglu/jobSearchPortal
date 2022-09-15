from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import uuid


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_photos/%Y/%m/',
                                      default='user-default.png')
    gender_choices = [("F", "Female"), ("M", "Male")]
    gender = models.CharField(choices=gender_choices, max_length=5, default=False, null=True, blank=True,
                              verbose_name='Gender')
    education_choices = [("1", "High School"), ("2", "Associate Degree"), ("3", "License"), ("4", "Postgraduate"), ("5", "Doctor")]
    education = models.CharField(choices=education_choices, max_length=13, default=False, null=True, blank=True,
                                 verbose_name='Education')
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super(ProfileModel, self).save()
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)

    @property
    def imageURL(self):
        try:
            url =self.profile_image.url
        except:
            url =''
        return url


class Skill(models.Model):
    owner = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Skills'

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['is_read','-created']

    def __str__(self):
        return self.subject
