from django import forms
from .models import UserProfile

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    avatar = forms.ImageField(label='Profile Photo', required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # The UserProfile is created via signals, so we just update it
        profile = user.userprofile
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()
