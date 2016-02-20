from django.shortcuts import render, get_object_or_404
from django.views.generic import View, UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from .forms import UserForm, CompletionStatusUpdateForm, GameOwnershipForm
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

class AddGamesView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    template_name = 'profiles/add_games.html'
    context_object_name = 'add_game_forms'

    def get_queryset(self):
        unaffiliated_games = self.request.user.gamebeaterprofile.get_unaffiliated_games()
        return [GameOwnershipForm(
            initial={"game": game, "owner": self.request.user.gamebeaterprofile}
        ) for game in unaffiliated_games]

class PreventGetMixin():
    """
    This mixin allows views to always refuse get requests. This is useful
    when a view should only process a POST and not display a form.
    """
    def get(self, request, *args, **kwargs):
        raise Http404

class GameOwnershipCreationView(LoginRequiredMixin, PreventGetMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    model = GameOwnership
    form_class = GameOwnershipForm

    success_url = reverse_lazy("profiles:add_games")

class CompletionStatusUpdateView(LoginRequiredMixin, PreventGetMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    model = GameOwnership
    form_class = CompletionStatusUpdateForm

    success_url = reverse_lazy("profiles:dashboard")

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
