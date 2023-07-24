from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagField

from .models import Post


class SignUpForm(UserCreationForm):
    """Sign up form. Email field added to standard UserCreationForm."""
    email = forms.EmailField(help_text='A valid email address, please.',
                             required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']


class EditProfile(forms.ModelForm):
    """Form for profile editing."""
    class Meta:
        model = get_user_model()
        fields = ['profile_image', 'username', 'first_name',
                  'last_name', 'email', 'bio']


class CreatePostForm(forms.ModelForm):
    """Form for post creating."""
    tags = TagField(help_text='Tags with commas.')

    class Meta:
        model = Post
        fields = ['description', 'tags']
