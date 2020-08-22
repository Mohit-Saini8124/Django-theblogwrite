from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), help_text="We'll never share your email with anyone else.")
	# email = forms.EmailField(widget=forms.EmailInput(
	# attrs={'class':'form-control', 'placeholder': 'Search' }),
	#  help_text="We'll never share your email with anyone else.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']	

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].help_text ='Password must contain at least 8 characters.'
		self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Invalid username and password."
                           " Note that both fields may be case-sensitive.")
			if not user.is_active:
				raise forms.ValidationError('User is not active')
		return super(UserLoginForm, self).clean(*args, **kwargs)



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name', 'email']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class':  'form-control'})
	

class ProfileUpdateForm(forms.ModelForm):
    website = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control', 'placeholder' : 'http://example.com'} ), required=False)
    facebookid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Facebook Id' }), required=False)
    twitterid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Twitter Id' }), required=False)
    instagramid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Instagram Id'}), required=False)
    about_us = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=False)
    hobbie = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	
    class Meta:
        model = Profile
        fields = ['image', 'website', 'facebookid', 'twitterid', 'instagramid', 'about_us', 'hobbie']

	
