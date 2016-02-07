from django.shortcuts import render, get_object_or_404
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from .forms import UserForm, CompletionStatusUpdateForm
from .models import GamebeaterProfile, GameOwnership

class DashboardView(LoginRequiredMixin, View):
	login_url = '/login'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# Handles display of Gamebeater Profile
		profile_pk = request.user.gamebeaterprofile.pk
		gamebeaterprofile = get_object_or_404(GamebeaterProfile, pk=profile_pk)
		gameownerships_by_completion_status_list = gamebeaterprofile.get_all_gameownerships_by_completion()
		return render(
			request,
			'profiles/dashboard.html',
			{
				"gamebeaterprofile": gamebeaterprofile,
				"gameownerships_by_completion_status_list": gameownerships_by_completion_status_list,
                "completion_status_update_form": CompletionStatusUpdateForm
			}
		)

class CompletionStatusUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    
    model = GameOwnership
    form_class = CompletionStatusUpdateForm
    
    success_url = reverse_lazy("profiles:dashboard")
    
    # Prevent a get from occuring. We only want this to be a post
    def get(self, request, *args, **kwargs):
        raise Http404

def register(request):
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			
			gamebeater_profile = GamebeaterProfile(user=user)
			gamebeater_profile.save()
			
			registered = True
		
		else:
			print user_form.errors
	else:
		user_form = UserForm()
	
	return render(
		request,
		'profiles/register.html',
		{'user_form': user_form, 'registered': registered}
	)
