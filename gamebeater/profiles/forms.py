from django import forms
from django.contrib.auth.models import User

from .utils import CompletionStatus 
from .models import GameOwnership

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class CompletionStatusUpdateForm(forms.ModelForm):

	class Meta:
		model = GameOwnership
		fields = ('completion_status',)