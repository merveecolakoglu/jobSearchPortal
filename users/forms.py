from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import ProfileModel, User, Skill, Message


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=60, label="Adı", widget=forms.TextInput(attrs={'placeholder': 'Adı'}))
    last_name = forms.CharField(max_length=60, label="Soyadı", widget=forms.TextInput(attrs={'placeholder': 'Soyadı'}))


class CustomUserCretionForm(UserCreationForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'username', 'email','password1','password2']

class ProfileForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['profile_image', 'gender', 'education', 'short_intro', 'bio', 'location',
                  'social_github',
                  'social_linkedin',
                  'social_twitter',
                  'social_website',
                  'social_youtube']


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
