"""
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile



from django import forms
from .models import Institution

class InstitutionSelectionForm(forms.ModelForm):
    '''
    Form for creating an instance related to a selected institution.
    '''
    first_name = forms.CharField(max_length=30, required=True,
    widget=forms.TextInput(attrs={'placeholder': '*Your first name..'}))
    institution_id = forms.CharField(max_length=30,required=True,
    widget=forms.TextInput(attrs='placeholder':'*Institution ID?...' ) )
    institution_name = forms.CharField(max_length=30,required=True,
    widget=forms.TextInput(attrs='placeholder':'*Institution name...' ) )
    address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    town = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    county = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    post_code = forms.CharField(max_length=8, required=True, widget = forms.HiddenInput())
    country = forms.CharField(max_length=40, required=True, widget = forms.HiddenInput())
    longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    class Meta:
        model = Institution
        fields = ['institution_name']
	#reCAPTCHA token
	  token = forms.CharField(
		widget=forms.HiddenInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
"""




# forms.py
from django import forms
from .models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['institution','review','review_image']



