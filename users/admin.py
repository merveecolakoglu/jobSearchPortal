from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import *

class UserModelAdmin(UserAdmin):
    list_display = ['username','first_name','last_name']

    class Meta:
        model =User

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user']

    class Meta:
        model =ProfileModel


admin.site.register(User,UserModelAdmin)
admin.site.register(ProfileModel,ProfileModelAdmin)
admin.site.register(Skill)
admin.site.register(Message)
