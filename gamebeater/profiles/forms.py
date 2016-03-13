from django import forms
from django.contrib.auth.models import User

from .statuses import CompletionStatus 
from .models import GameOwnership, Goal

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class CompletionStatusUpdateForm(forms.ModelForm):

	class Meta:
		model = GameOwnership
		fields = ('completion_status',)

class GameOwnershipForm(forms.ModelForm):

    class Meta:
        model = GameOwnership
        fields = ('owner', 'game', 'platform', 'ownership_status', 'completion_status')
        widgets = {'owner': forms.HiddenInput(), 'game': forms.HiddenInput}

class GameOwnershipUpdateForm(forms.ModelForm):

    class Meta:
        model = GameOwnership
        fields = ('platform', 'ownership_status', 'completion_status')

class GoalStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Goal
        fields = ('status',)

class GoalCreationForm(forms.ModelForm):

    class Meta:
        model = Goal 
        fields = ('ownership', 'text', 'start_time', 'complete_time', 'status')
        widgets = {'ownership': forms.HiddenInput(), 'start_time': forms.DateTimeInput(), 'complete_time': forms.DateTimeInput()}

class GoalCompletionStatusUpdateForm(forms.ModelForm):

	class Meta:
		model = Goal
		fields = ('status',)