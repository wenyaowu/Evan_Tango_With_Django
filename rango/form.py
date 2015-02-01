__author__ = 'evanwu'

from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm): # Inherit from forms.ModelForm
    name = forms.CharField(max_length=128, help_text="Type in the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)  # model will be responsible on save() to populating this field.
    # An inline class to provide additional information on the form.

    # We use this class to specify which field that we wish to include in our form
    # Through the field tuple
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',) # What is included to display in the form


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter the title of the page")
    url = forms.URLField(max_length=200, help_text="Enter the URL of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',) # What has been excluded from the form
        # Or, fields = ('title', 'url', 'views')

    #def clean(self):
    #    cleaned_data = self.clean_data # Cleaned_data is dictionary
    #    url = cleaned_data['url']

    #    if url and not url.startwith('http://'):
    #        url = 'http://'+url
    #        cleaned_data['url']=url
    #    return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')