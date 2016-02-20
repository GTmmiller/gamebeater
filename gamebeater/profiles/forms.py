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

class GameOwnershipForm(forms.ModelForm):

    class Meta:
        model = GameOwnership
        fields = ('owner', 'game', 'platform', 'ownership_status', 'completion_status')
        widgets = {'owner': forms.HiddenInput(), 'game': forms.HiddenInput}

    def clean_owner(self):
        if not self['owner'].html_name in self.data:
            return self.fields['owner'].initial
        return self.cleaned_data['owner']

    def clean_game(self):
        if not self['game'].html_name in self.data:
            return self.fields['game'].initial
        return self.cleaned_data['game']

    def __init__(self, *args, **kwargs):
        # filter options on a by game basis. Having every platform available
        # is overkill. TODO: consider always allowing latest gen platforms
        super(GameOwnershipForm, self).__init__(*args, **kwargs)
        if 'game' in self.initial:
            self.fields['platform'].queryset = self.initial['game'].platforms
