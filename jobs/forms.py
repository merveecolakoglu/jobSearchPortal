from django.forms import ModelForm
from .models import *
from django import forms


class JobForm(ModelForm):
    class Meta:
        model =JobModel
        fields =['title','featured_image','description','type','tags']

        widgets={
            'tags':forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ApplyJobForm(ModelForm):
    class Meta:
        model=ApplicantModel
        fields=['job']
